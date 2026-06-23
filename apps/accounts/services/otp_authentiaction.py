from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from apps.accounts.services.otp import OTPService
from django.core.exceptions import PermissionDenied


User = get_user_model()



class OTPAuthentication(BaseBackend):

    def authenticate(self, request, phone_number=None, otp_code=None, **kwargs):
        
        if not phone_number or not otp_code:
            return None
        
        otp_service = OTPService(phone_number)
        success, message = otp_service.verify_otp(otp_code)

        if not success:
            raise PermissionDenied(message)
        

        try:
            return User.objects.get(phone_number=phone_number, is_active=True)
        except User.DoesNotExist:
            return None
        

    
    def get_user(self, user_id):
        
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None
