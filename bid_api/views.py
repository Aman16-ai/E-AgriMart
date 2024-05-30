from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action,api_view
from middleware.custom_permission import CustomerOrReadOnlyPermission, CustomerOrOnlyFarmerBidLockPermission
from .serializers import *
from .service.RedisPubBid import RedisPubBid
from farmer.models import Bid
from rest_framework.exceptions import APIException
from .service.bid_dashboard_service import BidDashBoardService
from django_filters import rest_framework as filter
import json
class BidViewSet(viewsets.ModelViewSet):
    #Todo : add validatoin in partial update method that farmer can locked that bid that belongs to its crop
    queryset = Bid.objects.all()
    filter_backends = (filter.DjangoFilterBackend,)
    filterset_fields = {
        'crop':['exact'],
        'farmer':['exact'],
        'customer':['exact'],
    }
    permission_classes = [CustomerOrOnlyFarmerBidLockPermission]
    serializers = {
        'list' : GetBidModelSerializer,
        'create' : BidModelSerializer
    }
    def get_queryset(self):
        return Bid.objects.all().order_by('-bid_price')
    
    @action(detail=False,methods=['GET'])
    def get_dashboad_data(self,request,pk=None):
        try:
            product_id = request.GET['product_id']
            dashBoardService = BidDashBoardService(product_id=product_id,user=request.user)
            data = dashBoardService.getDashBoardData()
            print('data ------> data',data)
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail={"Error":"Something went wrong"})
    
    def perform_create(self, serializer):
        response = super().perform_create(serializer)

        # After creating the bid we have to publish it on redis channel. Channel is the crop id of that bid.
        instance = serializer.instance
        ser = GetBidModelSerializer(instance,many=False)
        pub = RedisPubBid()
        pub.pubBid(str(instance.crop.id),json.dumps(ser.data))
        
        return response
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'partial_update':
            return self.serializers['list']
        return self.serializers['create']
    def finalize_response(self, request, response, *args, **kwargs):
        final_response = Response({"status":response.status_code,"Response":response.data},status=response.status_code)
        final_response.accepted_renderer = request.accepted_renderer
        final_response.accepted_media_type = request.accepted_media_type
        final_response.renderer_context = self.get_renderer_context()
        return final_response
    
    def get_renderer_context(self):
        """
        Returns a dict that is passed through to Renderer.render(),
        as the `renderer_context` keyword argument.
        """
        # Note: Additionally 'response' will also be added to the context,
        #       by the Response object.
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None)
        }
