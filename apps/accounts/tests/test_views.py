from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import OTP, PendingRegistration


User = get_user_model()


class AuthViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('accounts:register_initiate')
        self.verify_url = reverse('accounts:register_verify')
        self.password_login_url = reverse('accounts:login_password')
        self.logout_url = reverse('accounts:logout')
        
        self.valid_register_data = {
            'phone_number': '09123456789',
            'first_name': 'spongebob',
            'last_name': 'squarepants',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'email': 'ali@example.com'
        }
    
    def _create_and_login_user(self):
        """Helper: Create user and get tokens."""
        user = User.objects.create_user(
            phone_number='09123456789',
            first_name='spongebob',
            last_name='squarepants',
            password='SecurePass123!'
        )
        refresh = RefreshToken.for_user(user)
        return user, str(refresh), str(refresh.access_token)
    
    def test_initiate_registration_success(self):
        """Test successful registration initiation."""
        response = self.client.post(
            self.register_url, 
            self.valid_register_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('message', response.data)
        self.assertTrue(PendingRegistration.objects.filter(
            phone_number='09123456789').exists())
        self.assertTrue(OTP.objects.filter(
            phone_number='09123456789').exists())



    def test_initiate_registration_duplicate_phone(self):
        """Test registration with already registered phone."""
        User.objects.create_user(
            phone_number='09123456789',
            first_name='Existing',
            last_name='User',
            password='password123'
        )
        
        response = self.client.post(
            self.register_url, 
            self.valid_register_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    


    def test_initiate_registration_invalid_data(self):
        """Test registration with invalid data."""
        invalid_data = {
            'phone_number': '09123456789',
            'first_name': '', 
            'last_name': 'squarepants',
            'password': 'weak',
            'password_confirm': 'different'
        }
        
        response = self.client.post(
            self.register_url, 
            invalid_data, 
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    



    def test_password_login_success(self):
        """Test successful password login."""

        User.objects.create_user(
            phone_number='09123456789',
            first_name='bob',
            last_name='squarepants',
            password='SecurePass123!'
        )
        
        response = self.client.post(
            self.password_login_url,
            {
                'phone_number': '09123456789',
                'password': 'SecurePass123!'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    


    def test_password_login_wrong_password(self):
        """Test login with wrong password."""
        User.objects.create_user(
            phone_number='09123456789',
            first_name='Ali',
            last_name='Mohammadi',
            password='SecurePass123!'
        )
        
        response = self.client.post(
            self.password_login_url,
            {
                'phone_number': '09123456789',
                'password': 'WrongPassword!'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('tokens', response.data)



    def test_logout_success(self):
        """Test successful logout."""
        user, refresh_token, access_token = self._create_and_login_user()
        
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        response = self.client.post(
            self.logout_url,
            {'refresh': refresh_token},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
    



    def test_logout_without_token(self):
        """Test logout without authentication."""
        response = self.client.post(
            self.logout_url,
            {'refresh': 'fake_token'},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class ProfileViewTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.profile_url = reverse('accounts:profile')
        self.change_password_url = reverse('accounts:change_password')
        
        self.user = User.objects.create_user(
            phone_number='09123456789',
            first_name='spongebob',
            last_name='squarepants',
            password='OldPass123!',
            email='ali@example.com'
        )
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_get_profile_success(self):
        """Test retrieving user profile."""
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'spongebob')
        self.assertEqual(response.data['last_name'], 'squarepants')
        self.assertEqual(response.data['phone_number'], '09123456789')
    



    def test_get_profile_unauthorized(self):
        """Test profile access without authentication."""
        self.client.credentials()  # Remove auth
        
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_change_password_success(self):
        """Test successful password change."""
        data = {
            'old_password': 'OldPass123!',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        }
        
        response = self.client.post(
            self.change_password_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
       
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass456!'))
    


    def test_change_password_wrong_old(self):
        """Test password change with wrong old password."""
        data = {
            'old_password': 'WrongPassword!',
            'new_password': 'NewPass456!',
            'confirm_password': 'NewPass456!'
        }
        
        response = self.client.post(
            self.change_password_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('OldPass123!'))