from django.contrib import admin
from django.urls import path,include
from customer.views import * 
urlpatterns = [
    path("page/",index),
    path("addbid/<int:pk>/",addBid)
]

