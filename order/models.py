from typing import Iterable
from django.db import models
from account.models import UserProfile,Address
from farmer.models import Product
# Create your models here.
STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('PROCESSING', 'PROCESSING'),
        ('SHIPPED', 'SHIPPED'),
        ('DELIVERED', 'DELIVERED'),
    )
class Order(models.Model):
    id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='order_customer')

    farmer = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='order_farmer')

    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="order_product")

    created_on = models.DateField(auto_now_add=True)

    address = models.ForeignKey(Address,on_delete=models.CASCADE,related_name="order_address",null=True,blank=True)
    
    status = models.CharField(choices=STATUS_CHOICES,max_length=20,default='PENDING')

    price = models.FloatField(null=True,blank=True)

    def save(self,*args, **kwargs):
        self.price = self.product.price
        super().save(*args,**kwargs)


