from django.contrib import admin
from django.urls import path,include
from farmer.views import * 
urlpatterns = [
    path("page/",index),
    path("predict/",predictProduction),
    path("handleprediction/",handlepredictedProduction),
    path("addProduct/",addProduct),
    path("bids/",fetchallbids)
]

