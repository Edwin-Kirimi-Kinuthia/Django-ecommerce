from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
import uuid
from .forms import UserRegisterForm, OTPForm, ForgotPasswordForm, ResetPasswordForm, ProfileUpdateForm
from .models import OTP, User, UnverifiedUser
from .utils import send_verification_email, send_otp
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, 'userauths/sign-up.html', {"form": form})

            unverified_user, created = UnverifiedUser.objects.update_or_create(
                email=email,
                defaults={
                    'username': username,
                    'password': make_password(password),
                    'registration_date': timezone.now(),
                    'verification_token': uuid.uuid4()
                }
            )
            
            send_verification_email(unverified_user, request)
            messages.success(request, f"Hello {username}, a verification link has been sent to your email.")
            return redirect('userauths:sign-in')
    else:
        form = UserRegisterForm()
    return render(request, 'userauths/sign-up.html', {"form": form})

def verify_email_view(request, token):
    unverified_user = get_object_or_404(UnverifiedUser, verification_token=token)
    
    if not unverified_user.is_valid():
        messages.error(request, "The verification link has expired. Please register again.")
        return redirect('userauths:sign-up')
    
    if User.objects.filter(email=unverified_user.email).exists():
        messages.error(request, "A user with this email already exists.")
        return redirect('userauths:sign-in')
    
    user = User.objects.create_user(
        username=unverified_user.username,
        email=unverified_user.email,
        password=unverified_user.password
    )
    
    unverified_user.delete()
    
    login(request, user)
    messages.success(request, "Your email has been verified and you are now logged in.")
    return redirect('core:index')

def verify_otp_view(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "Session expired. Please start the process again.")
                return redirect('userauths:sign-in')
            user = get_object_or_404(User, id=user_id)
            otp = OTP.objects.filter(user=user, otp=otp_code).last()
            if otp and otp.is_valid():
                if request.session.get('is_resetting_password'):
                    del request.session['is_resetting_password']
                    return redirect('userauths:reset-password')
                else:
                    messages.success(request, "OTP verified successfully.")
                    return redirect('userauths:reset-password')
            else:
                messages.error(request, "Invalid or expired OTP.")
    else:
        form = OTPForm()
    return render(request, 'userauths/verify-otp.html', {'form': form})

def verify_otp_link_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['user_id'] = user.id
        messages.success(request, "Please enter the OTP sent to your email.")
        return redirect('userauths:verify-otp')
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect('userauths:sign-in')

def resend_otp_view(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            send_otp(user, request)
            messages.success(request, "A new OTP has been sent to your email.")
        else:
            messages.error(request, "Session expired. Please start the process again.")
    return redirect('userauths:verify-otp')

def forgot_password_view(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_otp(user, request)
                request.session['user_id'] = user.id
                request.session['is_resetting_password'] = True
                messages.success(request, "An OTP has been sent to your email.")
                return redirect('userauths:verify-otp')
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'userauths/forgot-password.html', {'form': form})

def reset_password_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Session expired. Please start the password reset process again.")
        return redirect('userauths:forgot-password')

    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                del request.session['user_id']
                messages.success(request, "Your password has been reset successfully.")
                return redirect('userauths:sign-in')
            else:
                messages.error(request, "Passwords do not match.")
    else:
        form = ResetPasswordForm()
    return render(request, 'userauths/reset-password.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("core:index")
        else:
            messages.warning(request, "Invalid email or password. Please try again.")

    return render(request, "userauths/sign-in.html")

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have successfully logged out.")
    else:
        messages.warning(request, "You are not logged in.")
    return redirect("userauths:sign-in")

######################################################
@login_required
def profile_update_view(request):
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, user=user, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('userauths:profile-update')
    else:
        form = ProfileUpdateForm(user=user, instance=profile)

    return render(request, 'userauths/profile-update.html', {'form': form, 'user': user})