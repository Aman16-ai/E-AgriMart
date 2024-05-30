from pyexpat import model
from django.db import models
from account.models import UserProfile
from django.db.models import Q
from django.db.models import Avg,Count,Max
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.

status_choice = (
    ("Pending","Pending"),
    ("Selected","Selected"),
    ('Locked','Locked')
)

crop_quality_choice = (
    ('Good','Good'),
    ('Medium','Medium'),
    ('Low','Low')
)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(UserProfile,on_delete = models.CASCADE)
    title = models.CharField(max_length=250,null=True,blank=True)
    crop_img = models.ImageField(upload_to="crop_img")
    crop_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    quality = models.CharField(choices=crop_quality_choice,max_length=30,null=True,blank=True)
    
    def __str__(self):
        return self.crop_name
    
    def get_averageBidPrice(self):
        avg_price = Bid.objects.filter(crop=self.id).aggregate(Avg('bid_price'))['bid_price__avg']
        if avg_price != None:
            return avg_price or 0
        else:
            return 0
    
    def get_totalBids(self):
        return len(Bid.objects.filter(crop=self.id))
    
    def get_heighest_bid_price(self):
        heighest_bid_price = Bid.objects.filter(crop=self).aggregate(Max("bid_price"))['bid_price__max']
        return heighest_bid_price or 0
    
    @staticmethod
    def getFarmersTotalCrops(farmer,countOnly=False):
        allCrops = []
        if countOnly:
            allCrops = Product.objects.filter(farmer=farmer)
            return allCrops.count()
        return allCrops
    

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(UserProfile,default=None,on_delete = models.CASCADE,related_name="bid_farmer")
    customer = models.ForeignKey(UserProfile,on_delete = models.CASCADE,related_name="bid_coustmer")
    crop = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(choices = status_choice,max_length=20)
    bid_price = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    def __str__(self):
        return f"Bid by {self.customer.user.username}"
    
    @property
    def profit(self):
        return self.bid_price - self.crop.price
    
    @staticmethod
    def is_current_customer_added(user,crop):
        return Bid.objects.filter(Q(customer=user) & Q(crop=crop)).exists()

    @staticmethod
    def get_customer_lastest_bid(user,crop):
        try:
        # Retrieve bids for the specified customer and crop, ordered by timestamp in descending order
            bids = Bid.objects.filter(customer=user, crop=crop).order_by('-timestamp')
            if bids.exists():
                # Return the latest bid
                return bids.first()
            else:
                return None
        except ObjectDoesNotExist:
            return None
        
    @staticmethod
    def getFarmersTotalNumberOfLockedBids(farmer,countOnly=False):
        allBids = []
        if countOnly:
            allBids = Bid.objects.filter(farmer=farmer,status_choice='Locked')
            return allBids.count()
        return allBids

        
    
