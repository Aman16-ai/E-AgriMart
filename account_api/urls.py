from django.urls import include, path
from .views import *
from .router import accountRouter
urlpatterns = [
    path("getUser/",getUserDetails),
    path("",include(accountRouter.urls)),
]
