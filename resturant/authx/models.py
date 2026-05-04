from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser

from django.utils import timezone

# Create your models here.

#============================ Custom User =================
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(region="NP", unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"        #email baata login garna
    REQUIRED_FIELDS = ["username", "full_name", "phone_number"]     #superuser banauda

    class Meta:
        db_table = 'custom_user'





class Otp(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_otp")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()

    
    class Meta:
        db_table = 'otp'
     


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to="profile/", blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    # created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     self.created_at = timezone.now()
    #     return super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'profile'
  