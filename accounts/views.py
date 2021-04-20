from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants as level
from .forms import UserRegistrationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from listings.models import Enquiry


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("accounts:dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')


def logout(request):
    auth_logout(request)
    return redirect('pages:home')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful. Login with your credentials")
            return redirect('accounts:login')
        messages.add_message(request, level.ERROR, list(form.error_messages.values())[0])
    return render(request, 'accounts/register.html')


def dashboard(request):
    if request.user.is_authenticated:
        user_enquiries = Enquiry.objects.filter(user_id=request.user.id)[:]
        return render(request, 'accounts/dashboard.html', {
            'activated': 'Dashboard',
            'enquiries': user_enquiries
        })
    return redirect("accounts:login")


def response_with_error(request, template, message):
    messages.error(request, message)
    return render(request, template)
