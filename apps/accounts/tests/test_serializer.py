from django.contrib.auth import get_user_model
from django.test import TestCase
from apps.accounts.api.serializers.auth import (
    PasswordLoginSerializer,
    SendLoginOTPSerializer,
    VerifyLoginOTPSerializer,
    InitiateRegistrationSerializer,
)
from apps.accounts.api.serializers import profile 


User = get_user_model()


class PasswordLoginSerializerTest(TestCase):




    def test_valid_data(self):
        """Test serializer accepts valid phone and password."""
        data = {'phone_number': '09123456789', 'password': 'testpass123'}
        serializer = PasswordLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())




    def test_invalid_phone_number(self):
        """Test invalid phone format rejected."""
        data = {'phone_number': '12345', 'password': 'testpass123'}
        serializer = PasswordLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('phone_number', serializer.errors)


class SendLoginOTPSerializerTest(TestCase):



    def test_valid_phone(self):
        """Test valid phone accepted."""
        data = {'phone_number': '09123456789'}
        serializer = SendLoginOTPSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class VerifyLoginOTPSerializerTest(TestCase):



    def test_valid_code(self):
        """Test valid 6-digit code accepted."""
        data = {'code': '123456'}
        serializer = VerifyLoginOTPSerializer(data=data)
        self.assertTrue(serializer.is_valid())




    def test_code_too_short(self):
        """Test code less than 6 digits rejected."""
        data = {'code': '123'}
        serializer = VerifyLoginOTPSerializer(data=data)
        self.assertFalse(serializer.is_valid())





class InitiateRegistrationSerializerTest(TestCase):
    
    def setUp(self):
        self.valid_data = {
            'phone_number': '09123456789',
            'first_name': 'spongebob',
            'last_name': 'squarepants',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'email': 'ali@example.com'
        }
    



    def test_valid_registration_data(self):
        """Test serializer accepts valid data."""
        serializer = InitiateRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
    



    def test_passwords_do_not_match(self):
        """Test mismatched passwords rejected."""
        self.valid_data['password_confirm'] = 'DifferentPass!'
        serializer = InitiateRegistrationSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', str(serializer.errors))
    



    def test_empty_first_name(self):
        """Test empty first name rejected."""
        self.valid_data['first_name'] = ''
        serializer = InitiateRegistrationSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
    



    def test_empty_last_name(self):
        """Test empty last name rejected."""
        self.valid_data['last_name'] = '   '  # Whitespace only
        serializer = InitiateRegistrationSerializer(data=self.valid_data)
        self.assertFalse(serializer.is_valid())
    



    def test_password_confirm_removed(self):
        """Test password_confirm is removed from validated_data."""
        serializer = InitiateRegistrationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('password_confirm', serializer.validated_data)




class UserProfileSerializerTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='09123456789',
            first_name='spongebob',
            last_name='squarepants',
            password='testpass123',
            email='ali@example.com'
        )
    
    def test_phone_number_is_read_only(self):
        """Test phone number cannot be changed."""
        data = {'phone_number': '09987654321', 'first_name': 'Updated'}
        serializer = profile.UserProfileSerializer(
            instance=self.user, data=data, partial=True
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, '09123456789')


class ChangePasswordSerializerTest(TestCase):
    
    def test_passwords_do_not_match(self):
        """Test mismatched passwords rejected."""
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass456!',
            'confirm_password': 'DifferentPass!'
        }
        serializer = profile.ChangePasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_valid_password_change(self):
        """Test valid password data accepted."""
        data = {
            'old_password': 'oldpass123',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        }
        serializer = profile.ChangePasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())