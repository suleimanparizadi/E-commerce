from django.urls import path
from .views import  auth, profile

app_name = 'accounts'


urlpatterns = [
    # Registration
    path('register/initiate/', auth.InitiateRegistrationView.as_view(), name='register-initiate'),
    path('register/verify/', auth.VerifyRegistrationView.as_view(), name='register-verify'),
    
    # Login
    path('login/password/', auth.PasswordLoginView.as_view(), name='login-password'),
    path('login/otp/send/', auth.SendLoginOTPView.as_view(), name='login-otp-send'),
    path('login/otp/verify/', auth.VerifyLoginOTPView.as_view(), name='login-otp-verify'),
    
    # Logout
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', profile.ProfileView.as_view(), name='profile'),
    
    # Password
    path('password/change/', profile.ChangePasswordView.as_view(), name='change-password'),
]