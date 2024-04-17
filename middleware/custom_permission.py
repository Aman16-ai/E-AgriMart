from rest_framework.permissions import BasePermission
from account.models import UserProfile
from django.contrib.auth.models import AnonymousUser
class CustomerPermission(BasePermission):

    def has_permission(self, request, view):
        # user_profile_instance = UserProfile.objects.get(user = request.user)
        return request.user.groups.filter(name='Customer').exists()
        
class FarmerPermission(BasePermission):

    def has_permission(self, request, view):
        user_profile_instance = UserProfile.objects.get(user = request.user)
        if(user_profile_instance.user_type == 'Farmer'):
            return True
        else:
            return request.user.groups.filter(name='Farmer').exists()
        
class FarmerOrReadOnlyPermission(BasePermission):

    message = "Authentication credentials were not provided."
    def has_permission(self, request, view):
        
        try:
            if request.method == 'GET':
                return True
            else:
                if(isinstance(request.user,AnonymousUser)):
                    return False
                else:
                    if(request.user.groups.filter(name="Farmer").exists()):
                        return True
                    else:
                        self.message = "Only farmer is allowed to post crops"
                        return False

        except Exception as e:
            print(e)
            return False
        
class CustomerOrReadOnlyPermission(CustomerPermission):
    def has_permission(self, request, view):
        if(request.method == 'GET'):
            return True
        return super().has_permission(request, view)
    

class CustomerOrOnlyFarmerBidLockPermission(CustomerOrReadOnlyPermission):
    def has_permission(self, request, view):
        if((request.method == 'PATCH' or request.method == 'PUT') and FarmerPermission().has_permission(request=request,view=view)):
            if(request.data['status'] == 'Locked'):
                return True
            return False

        return super().has_permission(request, view)