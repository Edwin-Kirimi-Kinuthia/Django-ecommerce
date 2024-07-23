from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings

User= settings.AUTH_USER_MODEL

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hello {username}, your account was created successfully!")
            new_user = authenticate(email=form.cleaned_data["email"], password=form.cleaned_data["password1"])
            if new_user is not None:
                login(request, new_user)
            return redirect("core:index")
        else:
            messages.error(request, "There was an error with your registration. Please check the form for errors.")
    else:
        form = UserRegisterForm()

    return render(request, 'userauths/sign-up.html', {"form": form})

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

