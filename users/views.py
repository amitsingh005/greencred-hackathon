from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def home_page(request):
    return render(request, 'home.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/dashboard/')

    return render(request, 'login.html')


def signup_page(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('/dashboard/')

    return render(request, 'signup.html')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_page(request):
    return render(request, 'dashboard.html')