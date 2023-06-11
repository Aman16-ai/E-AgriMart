from django.urls import include, path
from .views import *
from .router import accountRouter
urlpatterns = [
    path("register/",createAccount),
    path("",include(accountRouter.urls))
]
