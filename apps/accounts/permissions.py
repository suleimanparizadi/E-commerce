from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model


User = get_user_model()



class IsAuthenticatedAndVerified(permissions.BasePermission):
    
    
    message = "You must be authenticated and have a verified account."

    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False # return the message as an error message
        
        if not request.user.is_active:
            raise PermissionDenied("Your account has been deactivated.")
                                    # return this instead the message
        return True
    


class IsAdmin(permissions.BasePermission):

    message = "Only admin users can perform this action."

    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False
        

        return request.user.is_admin
    


class IsOwner(permissions.BasePermission):
    """ Object-level permission to only allow owners of an object to edit it."""


    def has_object_permission(self, request, view, obj):
        
        if request.user.is_admin:
            return True
        

        if isinstance(obj, User):
            return obj == request.user
        

        raise PermissionDenied("You can only access your own data.")

