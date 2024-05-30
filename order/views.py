from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from middleware.custom_permission import IsCustomerOrBidOwner
from farmer.models import Bid
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from account.models import UserProfile,Address
from .serializer import OrderSerializer
# Create your views here.

class CreateOrderApiView(APIView):
    permission_classes = [IsAuthenticated,IsCustomerOrBidOwner]

    def post(self,request):
        #Todo : bid must be locked, get address id from payload and change the status of ordered product
        bid = Bid.objects.get(pk=request.data.get('bid_id'))
        self.check_object_permissions(request,bid)
        customer = bid.customer
        farmer = bid.farmer
        product = bid.crop
        order = Order(customer=customer,farmer=farmer,product=product)
        order.save()
        serializer = OrderSerializer(order,many=False)
        return Response(status=status.HTTP_201_CREATED,data={"status":True,'Response':serializer.data})


