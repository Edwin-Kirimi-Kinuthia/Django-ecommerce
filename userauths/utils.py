import random
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .models import OTP

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(user, request):
    otp = generate_otp()
    OTP.objects.filter(user=user).delete() 
    OTP.objects.create(user=user, otp=otp)
    
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse('userauths:verify-otp-link', kwargs={'uidb64': uid, 'token': token})
    )
    
    context = {
        'user': user,
        'otp': otp,
        'verification_link': verification_link
    }
    
    email_subject = 'Your OTP Code and Verification Link'
    email_body = render_to_string('userauths/otp-email.html', context)
    
    send_mail(
        email_subject,
        email_body,
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

def send_verification_email(unverified_user, request):
    verification_link = request.build_absolute_uri(
        reverse('userauths:verify-email', kwargs={'token': unverified_user.verification_token})
    )
    
    context = {
        'username': unverified_user.username,
        'verification_link': verification_link
    }
    
    email_subject = 'Verify Your Email'
    email_body = render_to_string('userauths/verification-email.html', context)
    
    send_mail(
        email_subject,
        email_body,
        'from@example.com',
        [unverified_user.email],
        fail_silently=False,
    )
