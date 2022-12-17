from django.contrib import admin
from django.urls import path,include
from customer.views import * 
urlpatterns = [
    path("page/",index),
    path("addbid/<int:pk>/",addBid),
    path("crop/<int:pk>/",crop_detail),
    path("updateBid/<int:pk>/",updateBid)
]

