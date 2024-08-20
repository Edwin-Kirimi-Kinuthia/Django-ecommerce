from django.db import models
from django.utils import timezone
from datetime import timedelta
from shortuuid.django_fields import ShortUUIDField
import uuid
from django.utils.html import mark_safe

def user_directory_path(instance, filename):
    return 'profiles/user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email= models.EmailField(unique=True)
    username= models.CharField(max_length=100)

    USERNAME_FIELD= "email"
    REQUIRED_FIELDS= ["username"]

    def __str__(self) -> str:
        return self.username
    

class UnverifiedUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128) 
    registration_date = models.DateTimeField(default=timezone.now)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = "Unverified User"
        verbose_name_plural = "Unverified Users"

    def is_valid(self):
        return timezone.now() < self.registration_date + timezone.timedelta(hours=24)
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    

class OTP(models.Model):
    otpid = ShortUUIDField(unique=True, length=6, max_length=10, prefix="OTP", alphabet="abcdefghijklmnopqrstuvwxyz1234567890")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "OTPs"

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=15)
    
    def __str__(self):
        return self.otpid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=user_directory_path, default="default_profile.jpg")
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def display_profile_image(self):
        return mark_safe('<img src="%s" width= "50" height= "50"/>' % (self.profile_image.url))
