from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.services.registration import RegistrationsService
from apps.accounts.models.OTPModel import OTP
from apps.accounts.models.pending_registration import PendingRegistration
from datetime import timedelta
from django.utils import timezone


User = get_user_model() 


class RegistrationServiceTest(TestCase):
    
    def setUp(self):
        self.phone_number = '09123456789'
        self.service = RegistrationsService(self.phone_number)
        self.valid_data = {
            'first_name': 'spongebob',
            'last_name': 'squarepants',
            'password': 'securepass123',
            'email': 'bob@example.com',
            'date_of_birth': '1990-01-01'
        }
        
    def test_initiate_registration_success(self):
        
        service = self.service
        success, message = service.initiate_registration(**self.valid_data)

        self.assertTrue(success)
        self.assertIn('sent successfully', message.lower())

        self.assertTrue(OTP.objects.filter(phone_number=self.phone_number).exists())
        




    def test_initiate_registration_duplicate_phone(self):
        User.objects.create_user(phone_number=self.phone_number, **self.valid_data)
        
        service = self.service
        success, message = service.initiate_registration(**self.valid_data)

        self.assertFalse(success)
        self.assertIn('already', message.lower())

        




    
    def test_initiate_registration_duplicate_email(self):
        User.objects.create_user(phone_number='09876543210', **self.valid_data)

        service = self.service
        success, message = service.initiate_registration(**self.valid_data)

        self.assertFalse(success)
        self.assertIn('already', message.lower())




    def test_initiate_registration_replaces_pending(self):
        
        PendingRegistration.objects.create(phone_number=self.phone_number, **self.valid_data)

        service = self.service
        success, message = service.initiate_registration(**self.valid_data)
        self.assertTrue(success)

        pending_count = PendingRegistration.objects.filter(phone_number=self.phone_number).count()

        self.assertEqual(pending_count, 1)


    def test_verification_failed(self):


        service = self.service
        service.initiate_registration(**self.valid_data)
        user, message = service.verify_and_create_user('000000')
        self.assertFalse(user)

        self.assertTrue(PendingRegistration.objects.filter(
            phone_number=self.phone_number).exists())




    def test_initiate_registration_missing_first_name(self):
        invalid_data = {
            'first_name': '',
            'last_name': 'squarepants',
            'password': '12234354',
            'email': 'bob@example.com',
            'date_of_birth': '1990-01-01'
        }      

        service = self.service
        success, message = service.initiate_registration(**invalid_data)

        self.assertFalse(success)
        self.assertIn('required', message.lower())
        






    def test_verify_and_create_pending_atomic_when_user_creation_fails(self):
        
        service = self.service
        service.initiate_registration(**self.valid_data)

        OTP.objects.update_or_create(
            phone_number=self.phone_number,
            defaults={
                'code':123456,
                'expired_at': timezone.now() + timedelta(minutes=3)
            }
        )

        User.objects.create_user(
        phone_number=self.phone_number, 
        first_name='patrick',
        last_name='star',
        password='password456'
        )

        user, message = service.verify_and_create_user(123456)

        self.assertFalse(user)
        the_otp = OTP.objects.filter(phone_number=self.phone_number).exists()
        self.assertTrue(PendingRegistration.objects.filter(
            phone_number=self.phone_number).exists())
        
        self.assertTrue(the_otp)

