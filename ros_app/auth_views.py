from logging import Logger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Account is inactive. Contact the admin for assistance.")
        else:
            messages.error(request, "Invalid login credentials.")

    return render(request, "pages/login.html")

@login_required
def home(request):
    # Logger.info(f"The user {request.user} accessed the dashboard.")
    return render(request, "pages/home.html", {"user": request.user})

@login_required
def user_logout(request):
    logout(request)
    return redirect("login")
