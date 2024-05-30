from django.urls import path
from .views import CreateOrderApiView

urlpatterns = [
    path("",CreateOrderApiView.as_view())
]
