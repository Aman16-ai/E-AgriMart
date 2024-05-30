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
from rest_framework.exceptions import APIException
# Create your views here.

class CreateOrderApiView(APIView):
    permission_classes = [IsAuthenticated,IsCustomerOrBidOwner]

    def checkOrderAlreadyCreated(self,customer,product):
        order = Order.objects.filter(customer=customer,product=product).exists()
        if(order):
            raise APIException({'message':"order already created"})
        return False
    def post(self,request):
        #Todo : bid must be locked, get address id from payload and change the status of ordered product and remove all the logic code inside the service layer
        try:
            bid = Bid.objects.get(pk=request.data.get('bid_id'))
            customer = bid.customer
            farmer = bid.farmer
            product = bid.crop
            if(not self.checkOrderAlreadyCreated(customer=customer,product=product)):
                self.check_object_permissions(request,bid)   
                order = Order(customer=customer,farmer=farmer,product=product)
                order.save()
                product.status = "ordered"
                product.save()
                serializer = OrderSerializer(order,many=False)
                return Response(status=status.HTTP_201_CREATED,data={"status":True,'Response':serializer.data})
            return Response(status=status.HTTP_409_CONFLICT,data={'Error':"Already created"})
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_409_CONFLICT,data={'Error':str(e)})


