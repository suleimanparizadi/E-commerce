from django.urls import path
from .views import  auth, profile

app_name = 'accounts'


urlpatterns = [
    # Registration
    path('register/initiate/', auth.InitiateRegistrationView.as_view(), name='register_initiate'),
    path('register/verify/', auth.VerifyRegistrationView.as_view(), name='register_verify'),
    
    # Login
    path('login/password/', auth.PasswordLoginView.as_view(), name='login_password'),
    path('login/otp/send/', auth.SendLoginOTPView.as_view(), name='login_otp_send'),
    path('login/otp/verify/', auth.VerifyLoginOTPView.as_view(), name='login_otp_verify'),
    
    # Logout
    path('logout/', auth.LogoutView.as_view(), name='logout'),
    
    # Profile
    path('profile/', profile.ProfileView.as_view(), name='profile'),
    
    # Password
    path('password/change/', profile.ChangePasswordView.as_view(), name='change_password'),


    # Admin
    path('admin/user_list/', auth.ListUsersView.as_view(), name='users_list'),
    path('admin/user_detail/<int:user_id>/', auth.DetailUserView.as_view(),
                                                            name='user_detail'),
    path('admin/user_activation/<int:user_id>/', auth.UserToggleActiveView.as_view(),
                                                                name='user_activation'),



]