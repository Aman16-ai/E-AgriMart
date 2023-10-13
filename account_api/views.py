from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .serializer import RegisterationSerializer,LoginSerializer, FarmerRegistrationSerializer,FarmerDetailsSerializer,UserDetailsSerializer
from account.models import UserProfile,FarmerProfile
from django.contrib.auth import authenticate
from utils.jwtUtil import get_tokens_for_user
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
class AccountViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = RegisterationSerializer

    @action(detail=False,methods=['POST'])
    def registerUser(self,request):
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            userprofileobj = serializer.create(validated_data=request.data)
            token = get_tokens_for_user(userprofileobj.user)

            return Response({**serializer.data,**token})
        return Response(serializer.errors)
    
    @action(detail=False,methods=['POST'])
    def loginUser(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.data
            user = authenticate(username=data['username'],password=data['password'])
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(token)
            else:
                return Response({"User not found"})
        else:
            return Response(serializer.error_messages)

    
    @action(detail=False,methods=['POST'])
    def registerFarmer(self,request):
        serializer = FarmerRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            farmer_profile_instance = serializer.save()
            token = get_tokens_for_user(farmer_profile_instance.userProfile.user)
            return Response({**serializer.data,**token})
        return Response({serializer.error_messages})

    
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
    

class FarmerAccountViewSet(viewsets.ModelViewSet):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerRegistrationSerializer

    action_serializers = {
        'list' : FarmerDetailsSerializer,
        'retrieve' : FarmerDetailsSerializer,
        'create' : FarmerRegistrationSerializer
    }
    
    @action(detail=False,methods=['POST'])
    def registerFarmer(self,request):
        serializer = FarmerRegistrationSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            farmer_profile_instance = serializer.save()
            token = get_tokens_for_user(farmer_profile_instance.userProfile.user)
            return Response({**serializer.data,**token})
        return Response({serializer.error_messages})
    
    def get_serializer_class(self):
        print('running outside')
        if hasattr(self, 'action_serializers'):
            print('running')
            return self.action_serializers.get(self.action, self.serializer_class)
    
    
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
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserDetails(request):
    print("Running get user")
    try:
        serializer = UserDetailsSerializer(UserProfile.objects.get(user=request.user),many=False)
        return Response({"Response":serializer.data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error" : "something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
