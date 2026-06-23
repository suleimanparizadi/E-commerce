from rest_framework import views, status
from rest_framework.response import Response
from apps.accounts.api.serializers import profile 
from apps.accounts.services import  password_service
from apps.accounts.permissions import IsAuthenticatedAndVerified



class ProfileView(views.APIView):

    permission_classes = [IsAuthenticatedAndVerified]

    def get(self, request):

        serializer = profile.UserProfileSerializer(request.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def patch(self, request):
        """Update current user's profile."""
        serializer = profile.UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)   




class ChangePasswordView(views.APIView):
    
    permission_classes = [IsAuthenticatedAndVerified]
    
    def post(self, request):
        serializer = profile.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        service = password_service(request.user)
        success, message = service.change_password(
            old_password=serializer.validated_data['old_password'],
            new_password=serializer.validated_data['new_password'],
            confirm_password=serializer.validated_data['confirm_password']
        )
        
        return Response(
            {'message': message},
            status=status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
        )


