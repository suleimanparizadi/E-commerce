from django.db import models 
from django.contrib.auth.hashers import make_password, identify_hasher
from datetime import timedelta
from django.utils import timezone


class PendingRegistration(models.Model):

    EXPIRY_MINUTES = 10 



    phone_number = models.CharField(max_length=11, unique=True)

    first_name = models.CharField(max_length=125, blank=False)
    last_name = models.CharField(max_length=125, blank=False)

    email = models.EmailField(max_length=225, blank=True, null=True, unique=True)
    password = models.CharField(max_length=128)
   
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    expired_at = models.DateTimeField(null=True, blank=True)



    def save(self, *args, **kwargs):

        try:
            identify_hasher(self.password) # to identify the password been hashed 
        except ValueError:
            self.password = make_password(self.password)

        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=self.EXPIRY_MINUTES)

        super().save(*args, **kwargs)


    def is_expired(self):
        return timezone.now() > self.expired_at


       
    def __str__(self):
        return f"{self.phone_number} - {self.last_name}"
    

