from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from action.models import EcoAction, AIVerification
from .ai_service import analyze_image

from django.contrib.auth.models import User
from django.db.models import Sum
from action.models import EcoAction

import base64
from django.core.files.base import ContentFile
from .ai_service import analyze_image
from .models import UserProfile

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

        # ✅ check if username exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                "error": "Username already exists"
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/dashboard/')

    return render(request, 'signup.html')

from django.contrib.auth.decorators import login_required

@login_required
def dashboard_page(request):
    return render(request, 'dashboard.html')
@login_required
def profile_page(request):
    profile = request.user.userprofile

    return render(request, 'profile.html', {
        "profile": profile
    })



def actions_page(request):
    result_data = None
    error = None

    if request.method == "POST":
        image_data = request.POST.get("image_data")

        try:
            if image_data:
                # 🔥 Convert base64 → image file
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]

                file = ContentFile(base64.b64decode(imgstr), name='capture.' + ext)

                # 🔥 AI analysis
                result_data = analyze_image(file)

        except Exception as e:
            error = str(e)

    return render(request, 'actions.html', {
        "result": result_data,
        "error": error
    })

@login_required
def leaderboard_page(request):
    users = UserProfile.objects.all().order_by('-green_credits')

    current_user = request.user.userprofile

    # rank calculation
    rank = list(users).index(current_user) + 1

    return render(request, 'leaderboard.html', {
        "users": users[:10],   # top 10
        "rank": rank,
        "me": current_user
    })

def leaderboard_page(request):
    leaderboard = (
        User.objects
        .annotate(total_points=Sum('ecoaction__credits_awarded'))
        .order_by('-total_points')
    )

    return render(request, 'leaderboard.html', {
        'leaderboard': leaderboard
    })