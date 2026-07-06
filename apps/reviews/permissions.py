from rest_framework import permissions




class IsOwnerOrAdmin(permissions.BasePermission):

    message = "you can't change other users review"

    def has_object_permission(self, request, view, obj):


        return request.user.is_admin or obj.user == request.user
    




class HasPurchasedProduct(permissions.BasePermission):

    message = "only purchase user's allow to write a review"


    def has_permission(self, request, view):
        
        """
            after order app is completed
        """

        ...

