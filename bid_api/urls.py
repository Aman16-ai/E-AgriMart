from django.urls import include, path
from .views import *
from .router import bidRouter
urlpatterns = [
    path("",include(bidRouter.urls))
]
