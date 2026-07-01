from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.services.registration import RegistrationsService

User = get_user_model() 


class RegistrationServiceTest(TestCase):
    
    def setUp(self):
        self.phone_number = '09123456789'
        self.service = RegistrationsService(self.phone_number)
        self.valid_data = {
            'first_name': 'spongebob',
            'last_name': 'squarepants',
            'password': 'securepass123',
            'email': 'ali@example.com',
            'date_of_birth': '1990-01-01'
        }


        # 1. Successful registration initiation
    def test_initiate_registration_success(self):
        # Create PendingRegistration + Send OTP
        # Assert: success=True, PendingRegistration exists, OTP created
        ...

    # 2. Duplicate phone number (already registered User)
    def test_initiate_registration_duplicate_phone(self):
        # Create existing User, try to register again
        # Assert: raises ValidationError

        ...


    # 3. Duplicate email
    def test_initiate_registration_duplicate_email(self):
        # Create User with same email, try to register
        # Assert: raises ValidationError
        ...


    # 4. Replace existing PendingRegistration
    def test_initiate_registration_replaces_pending(self):
        # Create PendingRegistration, initiate again
        # Assert: old pending deleted, new one created, only 1 exists
        ...


    # 5. OTP sending fails
    def test_initiate_registration_otp_fails(self):
        # Mock OTPService to return False
        # Assert: success=False, no PendingRegistration saved (atomic!)
        ...


    # 6. Missing required fields (test each)
    def test_initiate_registration_missing_first_name(self):
        # Assert: raises error

        ...