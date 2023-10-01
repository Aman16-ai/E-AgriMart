from rest_framework import viewsets
from middleware.custom_permission import FarmerPermission,FarmerOrReadOnlyPermission
from rest_framework.permissions import IsAuthenticated
from account.models import CropDetail,UserProfile
from .serializer import CropsModelSerializer, ProductCreateModelSerializer, ProductModelSerializer
from rest_framework.response import Response
from farmer.models import Product
class CropsViewSet(viewsets.ModelViewSet):
    queryset = CropDetail.objects.all()
    serializer_class = CropsModelSerializer
    # permission_classes = [FarmerPermission]

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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [FarmerOrReadOnlyPermission]
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateModelSerializer
        return ProductModelSerializer
    
    
    
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
    