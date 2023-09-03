from rest_framework.permissions import BasePermission
from account.models import UserProfile
class CustomerPermission(BasePermission):

    def has_permission(self, request, view):
        user_profile_instance = UserProfile.objects.get(user = request.user)
        if(user_profile_instance.user_type == 'Customer'):
            return True
        else:
            return request.user.groups.filter(name='Customer').exists()
        
class FarmerPermission(BasePermission):

    def has_permission(self, request, view):
        user_profile_instance = UserProfile.objects.get(user = request.user)
        if(user_profile_instance.user_type == 'Farmer'):
            return True
        else:
            return request.user.groups.filter(name='Farmer').exists()