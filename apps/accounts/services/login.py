from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from apps.accounts.services.otp import OTPService

User = get_user_model()



class PasswordLoginService:

    """
        Handles phone number + password login.
        Returns JWT tokens on success.
        """


    def __init__(self, phone_number, password):
        self.phone_number = phone_number
        self.password = password



    def login(self):

        try:
            user = User.objects.get(phone_number=self.phone_number)        
       
        except User.DoesNotExist:
            return False, "Invalid phone number or password."        
        
        if not user.is_active:
            return False, "This account has been deactivated."
        

        if not user.check_password(self.password):
            return False, "Invalid phone number or password."
        

        user.update_last_login()
        

        return True, user
    


class OTPLoginService:

    def __init__(self, phone_number):
        self.phone_number = phone_number


    def send_otp(self):

        if  User.objects.filter(phone_number=self.phone_number, is_active=True).exists():

            otp_service = OTPService(self.phone_number)

            success, message = otp_service.create_otp()

            if success:
                return True, message
            
            return False, message
      

        return False, "Unable to process request. Please try again later."
            

    def verify_otp(self, input_code):


        otp_service = OTPService(self.phone_number)
        success, message = otp_service.verify_otp(input_code)


        if success:

            try:
                user = User.objects.get(phone_number=self.phone_number)
            except User.DoesNotExist:
                return None, "Accounts not found"
            
            
            user.update_last_login()

            return user, message
        
        return None, message
