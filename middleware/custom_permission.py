from rest_framework.permissions import BasePermission

class CustomerPermission(BasePermission):

    def has_permission(self, request, view):
        if(request.user.user_type == 'Farmer'):
            return True
        else:
            return request.user.groups.filter(name='Customer').exists()