from django.test import TestCase
from apps.accounts.models.OTPModel import OTP
from apps.accounts.services.otp import OTPService 
from django.utils import timezone
from datetime import timedelta



class OTPServiceTest(TestCase):


    def setUp(self):
        self.phone_number = '09123456789'
        self.otp_service = OTPService(self.phone_number)

        
    def test_create_otp(self):
        success , message = self.otp_service.create_otp()

        self.assertTrue(success)
        self.assertTrue(OTP.objects.filter(phone_number=self.phone_number).exists())

    
    def test_cooldown(self):
        self.otp_service.create_otp()
        
        
        success, message = self.otp_service.create_otp()

        otp_count = OTP.objects.filter(phone_number=self.phone_number).count()

        self.assertFalse(success)
        self.assertEqual(otp_count, 1)
        self.assertIn('please wait', message.lower())



    def test_verify_correct_otp(self):

        self.otp_service.create_otp()
        code = OTP.objects.get(phone_number=self.phone_number).code

        success, message = self.otp_service.verify_otp(code)

        self.assertTrue(success)
        self.assertIn('success', message.lower())
        self.assertFalse(OTP.objects.filter(
            phone_number=self.phone_number).exists())


    def test_verify_wrong_code(self):

        self.otp_service.create_otp()
        success, message = self.otp_service.verify_otp('000000')
        otp_attempt = OTP.objects.get(phone_number=self.phone_number).attempts

        self.assertFalse(success)
        self.assertIn('invalid code', message.lower())
        self.assertEqual(otp_attempt, 1)


    def test_verify_expired_otp(self):

        OTP.objects.update_or_create(
            phone_number=self.phone_number,
            defaults={
            'code':123456,
            'created_at':timezone.now() - timedelta(minutes=5),# create 5 minutes ago
            'expired_at':timezone.now() - timedelta(minutes=2) #expired 2 minutes ago
            }            
        )
        success, message = self.otp_service.verify_otp(123456)

        self.assertFalse(success)
        self.assertIn('expired', message.lower())
        self.assertFalse(OTP.objects.filter(
            phone_number=self.phone_number).exists())



    def test_max_attempt_delete_otp(self):

        self.otp_service.create_otp()

        self.otp_service.verify_otp('000000')
        self.otp_service.verify_otp('000000')
        success, message = self.otp_service.verify_otp('000000')


        self.assertFalse(success)
        self.assertIn('too many', message.lower())
        self.assertFalse(OTP.objects.filter(phone_number=self.phone_number).exists())



    def test_none_exist_otp(self):

        success, message = self.otp_service.verify_otp('123456')

        self.assertFalse(success)
        self.assertIn('no active', message.lower())