from pyexpat import model
from django.db import models
from account.models import UserProfile
from django.db.models import Avg,Count
# Create your models here.

status_choice = (
    ("Pending","Pending"),
    ("Selected","Selected")
)

crop_quality_choice = (
    ('Good','Good'),
    ('Medium','Medium'),
    ('Low','Low')
)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(UserProfile,on_delete = models.CASCADE)
    crop_img = models.ImageField(upload_to="crop_img")
    crop_name = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField()
    quality = models.CharField(choices=crop_quality_choice,max_length=30,null=True,blank=True)
    
    def __str__(self):
        return self.crop_name
    
    def get_averageBidPrice(self):
        return Bid.objects.filter(crop=self.id).aggregate(Avg('bid_price'))['bid_price__avg']
    
    def get_totalBids(self):
        return len(Bid.objects.filter(crop=self.id))
    

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    farmer = models.ForeignKey(UserProfile,default=None,on_delete = models.CASCADE,related_name="bid_farmer")
    customer = models.ForeignKey(UserProfile,on_delete = models.CASCADE,related_name="bid_coustmer")
    crop = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(choices = status_choice,max_length=20)
    bid_price = models.PositiveIntegerField()
    
    def __str__(self):
        return f"Bid by {self.customer.user.username}"
    
    @property
    def profit(self):
        return self.bid_price - self.crop.price
    