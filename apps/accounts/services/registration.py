from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from apps.accounts.models import PendingRegistration
from apps.accounts.services import otp
from django.db import IntegrityError

User = get_user_model()



class RegistrationsService:
    """
    Service to handle two step user registration with phone verification.
    
    
    1. initiate_registration() - Save data + Send OTP
    2. verify_and_create_user() - Verify OTP + Create User
    """


    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.otp_service = otp.OTPService(phone_number)

    @transaction.atomic # All happenned together or all cancelled togather 
    def initiate_registration(self, first_name, last_name, password,
                              email=None, date_of_birth=None):
        

        if User.objects.select_for_update().filter(phone_number=self.phone_number).first():
            return False, "this user is already registerd"

        if  not first_name :
            return False, 'first name is required.'
        
        if  not last_name :
            return False, 'last name is required.'


        if not password :
            return False, 'password is required.'

        if not self.phone_number :
            return False, 'phone number is required.'



        if email and User.objects.filter(email=email).exists():
            return False, "This email is already registered."
        


        PendingRegistration.objects.filter(phone_number=self.phone_number).delete()
       

        PendingRegistration.objects.create(
            phone_number=self.phone_number,
            first_name=first_name,
            last_name=last_name,
            password=password,  
            email=email,
            date_of_birth=date_of_birth
            
        )


        success, message = self.otp_service.create_otp()

        if success:
            return True, message
        
        return False, message
    

    @transaction.atomic
    def verify_and_create_user(self, code):


        try:
            pending = PendingRegistration.objects.get(phone_number=self.phone_number)

        except PendingRegistration.DoesNotExist:
            return False, "No pending registration found. Please start the registration process again."


        success, message = self.otp_service.verify_otp(code)

        if not success:
            return False, message
        
        try:
            user = User.objects.create_user(
                phone_number = self.phone_number,
                first_name = pending.first_name,
                last_name = pending.last_name,
                password = None,
                email=pending.email
            )
            user.password = pending.password

            if pending.date_of_birth:
                user.date_of_birth = pending.date_of_birth

            user.save(update_fields=['date_of_birth','password'])

            pending.delete()

            return user, message
        

                # to avoid go around database uniqueness 
        except IntegrityError:

            # Transaction is broken and will roll back automatically.
            # OTP deletion and any other changes are undone.

            return False, "A user with this email or phone number already exists."


