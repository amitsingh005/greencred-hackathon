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


@login_required
def actions_page(request):
    result_data = None
    error = None

    if request.method == "POST":
        photo = request.FILES.get('photo')

        # ❌ No file
        if not photo:
            error = "No file uploaded"
            return render(request, 'actions.html', {"error": error})

        # ✅ Create action first
        action = EcoAction.objects.create(
            user=request.user,
            action_type='plant_tree',
            photo=photo
        )

        try:
            # 🔥 IMPORTANT: reset file pointer
            photo.seek(0)

            # 🧠 AI ANALYSIS
            result = analyze_image(photo)

            confidence = result.get('confidence', 0)
            labels = result.get('labels', [])

            # 🎯 DECISION LOGIC
            if confidence > 0.7:
                status = 'verified'
                action.status = 'verified'
                action.credits_awarded = 50

                # ✅ UPDATE USER PROFILE (IMPORTANT)
                profile = request.user.userprofile
                profile.green_credits += 50
                profile.weekly_credits += 50
                profile.save()

            else:
                status = 'rejected'
                action.status = 'rejected'

            action.save()

            # 📊 SAVE AI RESULT
            AIVerification.objects.create(
                action=action,
                vision_confidence=confidence,
                detected_labels=", ".join(labels),
                verification_status=status
            )

            # 📦 RESPONSE DATA
            result_data = {
                "confidence": round(confidence, 2),
                "status": status,
                "labels": labels
            }

        except Exception as e:
            print("ACTION ERROR:", e)
            error = "AI processing failed"

    return render(request, 'actions.html', {
        "result": result_data,
        "error": error
    })

from .models import UserProfile

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