from django.urls import path
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name="sign-in"),
    path('sign-out/', views.logout_view, name="sign-out"),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),
    path('verify-email/<uuid:token>/', views.verify_email_view, name='verify-email'),
    path('verify-otp/<uidb64>/<token>/', views.verify_otp_link_view, name='verify-otp-link'),
    path('forgot-password/', views.forgot_password_view, name='forgot-password'),
    path('reset-password/', views.reset_password_view, name='reset-password'),
    path('resend-otp/', views.resend_otp_view, name='resend-otp'),
    path('profile-update/', views.profile_update_view, name='profile-update'),
]