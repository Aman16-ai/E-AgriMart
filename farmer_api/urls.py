from django.urls import include, path
from .views import *
from .router import simpleRouter
urlpatterns = [
    path("",include(simpleRouter.urls))
]
