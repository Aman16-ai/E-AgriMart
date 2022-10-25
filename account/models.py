from django.db import models
from django.contrib.auth.models import User
from django.forms import ChoiceField

# Create your models here.

user_type_choices = (
    ("Farmer","Farmer"),
    ("Customer","Customer")
)

city_choices = (
    ("Delhi","Delhi"),
    ("Mumbai","Mumbai"),
    ("Patna","Patna"),
    ("Itanagar","Itanagar")
)

State_choices = (
    ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
    ('Andhra Pradesh','Andhra Pradesh'),
    ("Arunachal Pradesh","Arunachal Pradesh"),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Delhi','Delhi'),
    ("Mumbai","Mumbai")
)

gender_choices = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other")
)

class Address(models.Model):
    id = models.AutoField(primary_key = True)
    pincode = models.IntegerField(blank=True, null=True)
    city = models.CharField(choices=city_choices,max_length=70,blank=True, null=True,)
    state = models.CharField(choices=State_choices,max_length=70,blank=True, null=True)
    landmark = models.CharField(max_length=70)
    
    def __str__(self):
        return self.city

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    user_type = models.CharField(choices=user_type_choices,max_length = 10)
    address = models.ForeignKey(Address,on_delete = models.CASCADE)
    contact_no = models.PositiveIntegerField()
    
    def __str__(self):
        return self.user.username
    # gender = ChoiceField(choices=gender_choices)
    


