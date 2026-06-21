from django.db import models
from django.utils import timezone
from datetime import timedelta



class OTP(models.Model):

    phone_number = models.CharField(max_length=11, unique=True)
    code = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)


    EXPIRY_TIME = 3 


    def is_expired(self):

        expiry_time = self.crreated_at + timedelta(minutes=self.EXPIRY_TIME)
        return timezone.now() > expiry_time


    def __str__(self):
        return f"{self.phone_number} - {self.code}"
        
