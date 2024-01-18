from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from middleware.custom_permission import CustomerOrReadOnlyPermission
from .serializers import *
from .service.RedisPubBid import RedisPubBid
from farmer.models import Bid
from rest_framework.exceptions import APIException
from .service.bid_dashboard_service import BidDashBoardService

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    # serializer_class = GetBidModelSerializer
    permission_classes = [CustomerOrReadOnlyPermission]
    # def get_queryset(self):
    #     rb = RedisPubBid()
    #     print('running')
    #     rb.pubBid("eargi","bid")
    #     return super().get_queryset()
    serializers = {
        'list' : GetBidModelSerializer,
        'create' : BidModelSerializer
    }

    @action(detail=True,methods=['GET'])
    def get_dashboad_data(self,request,pk=None):
        try:
            dashBoardService = BidDashBoardService(product_id=pk,user=request.user)
            data = dashBoardService.getDashBoardData()
            print('data ------> data',data)
            return Response({"Response":data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            raise APIException(detail={"Error":"Something went wrong"})
    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializers['list']
        return self.serializers['create']
    def finalize_response(self, request, response, *args, **kwargs):
        final_response = Response({"status":response.status_code,"Response":response.data})
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