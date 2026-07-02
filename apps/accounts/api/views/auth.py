from rest_framework import views, status
from rest_framework.response import Response
from apps.accounts.api.serializers import auth as auth_serializer
from apps.accounts.services import registration, login, token
from apps.accounts.permissions import IsAuthenticatedAndVerified
from rest_framework_simplejwt.tokens import RefreshToken


class InitiateRegistrationView(views.APIView):


    def post(self, request):

        serializer = auth_serializer.InitiateRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        service = registration.RegistrationsService(data['phone_number'])

        result, message = service.initiate_registration(
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            email=data.get('email'),
            date_of_birth=data.get('date_of_birth')

        )

        return Response({'message':message}, status=status.HTTP_202_ACCEPTED if result 
                        else status.HTTP_400_BAD_REQUEST)




class VerifyRegistrationView(views.APIView):


    def post(self, request):

        serializer = auth_serializer.VerifyLoginOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        service = registration.RegistrationsService(serializer.validated_data['phone_number'])
        result ,message = service.verify_and_create_user(serializer.validated_data['code'])
        if result:
            user_token = token.generate_token(result)

            return Response({'message':message,
                         'tokens':user_token},status=status.HTTP_201_CREATED)

        return Response({'message':message},status=status.HTTP_400_BAD_REQUEST)




class PasswordLoginView(views.APIView):


    def post(self, request):

        serializer = auth_serializer.PasswordLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = login.PasswordLoginService(
            serializer.validated_data['phone_number'],
            serializer.validated_data['password'])
        
        result, message = service.login()

        if result:
            user_token = token.generate_token(result)
       
            return Response({'tokens':user_token, 'message':message}, status=status.HTTP_200_OK)

        return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)
    

class SendLoginOTPView(views.APIView):


    def post(self, request):
        
        serializer = auth_serializer.SendLoginOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = login.OTPLoginService(serializer.validated_data['phone_number'])
        result, message = service.send_otp()

        return Response({'message':message},status=status.HTTP_200_OK)
    


class VerifyLoginOTPView(views.APIView):

    def post(self, request):
        serializer = auth_serializer.VerifyLoginOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = login.OTPLoginService(serializer.validated_data['phone_number'])
        
        result, message = service.verify_otp(serializer.validated_data['code'])
        
        
        if result:
            user_token = token.generate_token(result)

            return Response({'message':message, 'tokens':user_token},
                        status=status.HTTP_200_OK)

        return Response({'message':message}, status=status.HTTP_400_BAD_REQUEST)





class LogoutView(views.APIView):

    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request):

        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({'error':'refresh token is required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:
            return Response({"error": "Invalid token"},
                                                    status=status.HTTP_400_BAD_REQUEST)


        return Response({'message':'Logged out successfully'},
                                                        status=status.HTTP_200_OK)

    
