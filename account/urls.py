from django.contrib import admin
from django.urls import path,include
from account.views import *
urlpatterns = [
    path("register/",index,name="register"),
    path("register/signup",handleRegister,name="signup"),
    path("login/",loginpage),
    path("handlelogin",handleLogin),
    path("logout/",logoutuser),
    # path("api/",include("api.urls"))
]
