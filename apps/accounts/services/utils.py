from apps.accounts.models.otp import OTP
import random 
from django.utils import timezone



class OTPService:

    def __init__(self, phone_number):
        self.phone_number = phone_number


    def generate_code(self):
        
        
        return random.randint(111111, 999999)    


    def send_otp(self, code):

        """send otp via SMS
        Integrate with the SMS provider here."""

        print(f'the OTP{code} for {self.phone_number}')
        
        
        # return True or False based on SMS sending success
        return True
    
        
    def create_otp(self):
        code = self.generate_code()

        OTP.objects.update_or_create(
            phone_number = self.phone_number, # use this to find the record
            defaults= {'code': code, 'created_at':timezone.now()} # the value needs to update
        )

        self.send_otp(code)

        return code
    


    def verify_otp(self, input_code):

        if not input_code:
            return False, 'code is required.'
        
        try:
            otp = OTP.objects.get(phone_number=self.phone_number)
        except OTP.DoesNotExist:
            return False, 'cannot find the one time password for this number.'
        
        if otp.is_expired():
            otp.delete()

            return False, 'the one time password is expired.'
        

        try:
            input_code = int(input_code)

        except (ValueError, TypeError):
            return False, 'Invalid code format.'
        
        if otp.code != input_code:
            return False, 'Invalid code. try again.'
        

        otp.delete()
        return True, 'one time password verifier successfully.'
    
