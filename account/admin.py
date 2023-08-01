from django.contrib import admin
from account.models import UserProfile,Address,CropDetail,FarmerProfile
# Register your models here.
admin.site.register((UserProfile,Address,CropDetail,FarmerProfile))
