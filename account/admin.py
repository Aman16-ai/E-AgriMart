from django.contrib import admin
from account.models import UserProfile,Address
# Register your models here.
admin.site.register((UserProfile,Address))
