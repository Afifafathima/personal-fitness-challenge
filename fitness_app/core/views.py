from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .models import (
    User,
    Trainer,
    Challenge,
    JoinChallenge,
    Report,
    Activity,
    WeightLog,
    CalorieLog
)
from django.http import JsonResponse
from datetime import date, timedelta
from django.utils import timezone


# 🏠 HOME
def home(request):
    return render(request, "home.html")


# -------------------------
# 🔐 SIGNUP FLOW (PAGES)
# -------------------------
def signup1(request):
    return render(request, "signup/signup1.html")


def signup2(request):
    return render(request, "signup/signup2.html")


def signup_user(request):
    return render(request, "signup/signup-user.html")


def signup_trainer(request):
    return render(request, "signup/signup-trainer.html")


# -------------------------
# ✅ SIGNUP LOGIC
# -------------------------
def signup(request):
    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        certificate = request.POST.get("certificate")

        # 🚫 Prevent duplicate email
        if User.objects.filter(email=email).exists():
            return render(request, "signup/signup1.html", {
                "error": "Email already exists"
            })

        # 👤 Create user
        user = User.objects.create(
            name=name,
            email=email,
            password=password,
            role=role,
            specialization=request.POST.get(
                "specialization"
            ),
            experience=request.POST.get(
                "experience"
    
            )
        )

        # 🏋️ Trainer profile
        if role == "trainer":
            Trainer.objects.create(
                user=user,
                certificate=certificate,
                status="pending"
            )

        return redirect("/login/")

    return redirect("/signup1/")


# -------------------------
# 🔐 LOGIN PAGE
# -------------------------
def login_view(request):
    return render(request, "login.html")


# -------------------------
# 🔐 LOGIN LOGIC
# -------------------------
def login_user(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid credentials"
            })

        # ✅ STORE SESSION
        request.session["user_email"] = user.email
        request.session["role"] = user.role

        # ✅ ROLE REDIRECT
        if user.role == "admin":
            return redirect("/admin/dashboard/")

        elif user.role == "trainer":
            return redirect("/trainer/dashboard/")

        else:
            return redirect("/user/dashboard/")

    return redirect("/login/")


# -------------------------
# USER PAGES
# -------------------------
def user_dashboard(request):
    return render(request, "user/dashboard.html")


def user_challenges(request):
    return render(request, "user/challenges.html")


def user_challenge_detail(request):
    return render(request, "user/challenge-detail.html")


def user_profile(request):
    return render(request, "user/profile.html")


def user_help(request):
    return render(request, "user/help.html")


def user_leaderboard(request):
    return render(request, "user/leaderboard.html")


def user_trainers(request):
    return render(request, "user/trainers.html")


def user_trainer_detail(request):
    return render(request, "user/trainer-detail.html")


def user_calories(request):
    return render(request, "user/calories.html")


# -------------------------
# TRAINER PAGES
# -------------------------
def trainer_dashboard(request):
    return render(request, "trainer/dashboard.html")


def trainer_challenges(request):
    return render(request, "trainer/challenges.html")


# -------------------------
# CREATE CHALLENGE PAGE
# -------------------------
def create_challenge(request):

    # LOGIN CHECK
    if "user_email" not in request.session:
        return redirect("/login/")

    return render(
        request,
        "trainer/create-challenge.html"
    )


# -------------------------
# API - CREATE CHALLENGE
# -------------------------
def create_challenge_api(request):

    if request.method == "POST":

        # LOGIN CHECK
        if "user_email" not in request.session:

            return JsonResponse({
                "error": "Login required"
            })

        try:

            user = User.objects.get(
                email=request.session["user_email"]
            )

            trainer = Trainer.objects.get(
                user=user
            )

            # APPROVAL CHECK
            if trainer.status != "approved":

                return JsonResponse({
                    "error":
                    "Your trainer account is not approved yet"
                })

            name = request.POST.get("name")
            days = request.POST.get("days")
            image = request.POST.get("image")
            category = request.POST.get("category")

            challenge = Challenge.objects.create(
                trainer=trainer,
                name=name,
                days=days,
                image=image,
                category=category
            )

            Activity.objects.create(
                trainer=trainer,
                message=f"Created challenge: {challenge.name}"
            )

            return JsonResponse({
                "success": True
            })

        except:

            return JsonResponse({
                "error": "Something went wrong"
            })

    return JsonResponse({
        "error": "Invalid request"
    })


def trainer_leaderboard(request):
    return render(request, "trainer/leaderboard.html")


def trainer_profile(request):
    return render(request, "trainer/profile.html")


def trainer_help(request):
    return render(request, "trainer/help.html")


# -------------------------
# ADMIN PAGES
# -------------------------
def admin_dashboard(request):
    pending_trainers = Trainer.objects.filter(status="pending")
    return render(request, "admin/dashboard.html", {
        "trainers": pending_trainers
    })


def admin_manage_challenges(request):
    return render(request, "admin/manage-challenges.html")


def admin_reports(request):
    return render(request, "admin/reports.html")


def admin_certificate(request):
    pending_trainers = Trainer.objects.filter(status="pending")
    return render(request, "admin/certificate.html", {
        "trainers": pending_trainers
    })


# -------------------------
# APPROVE TRAINER
# -------------------------
def approve_trainer(request, id):
    trainer = Trainer.objects.get(id=id)
    trainer.status = "approved"
    trainer.save()

    return redirect("/admin/dashboard/")


# -------------------------
# API - GET CHALLENGES
# -------------------------
def get_challenges(request):

    challenges = Challenge.objects.all().order_by("-id")

    data = []

    for ch in challenges:

        data.append({
            "id": ch.id,
            "name": ch.name,
            "days": ch.days,
            "image": ch.image,
            "trainer": ch.trainer.user.name,
            "category": ch.category
        })

    return JsonResponse(data, safe=False)

# -------------------------
# API - SINGLE CHALLENGE
# -------------------------
def get_single_challenge(request, id):

    try:

        ch = Challenge.objects.get(id=id)

        joined_users = JoinChallenge.objects.filter(
            challenge=ch
        ).count()

        # CHECK IF USER JOINED
        joined_exists = False

        if "user_email" in request.session:

            try:

                user = User.objects.get(
                    email=request.session["user_email"]
                )

                joined_exists = JoinChallenge.objects.filter(
                    user=user,
                    challenge=ch
                ).exists()

            except:
                pass

        data = {

            "id": ch.id,

            "name": ch.name,

            "days": ch.days,

            "image": ch.image,

            "trainer": ch.trainer.user.name,

            "category": ch.category,

            "joined_users": joined_users,

            "joined": joined_exists,

            "description":
            f"""
            Join the {ch.name} challenge
            and improve your fitness journey
            with daily consistency and
            guided progress tracking.
            """
        }

        return JsonResponse(data)

    except:

        return JsonResponse({
            "error": "Challenge not found"
        })


# -------------------------
# JOIN CHALLENGE
# -------------------------
def join_challenge(request, id):

    if "user_email" not in request.session:
        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        challenge = Challenge.objects.get(id=id)

        existing = JoinChallenge.objects.filter(
            user=user,
            challenge=challenge
        )

        if existing.exists():

            existing.delete()

            return JsonResponse({
                "joined": False
            })

        else:

            JoinChallenge.objects.create(
                user=user,
                challenge=challenge
            )

            return JsonResponse({
                "joined": True
            })

    except:

        return JsonResponse({
            "error": "Something went wrong"
        })


# -------------------------
# REPORT CHALLENGE
# -------------------------
def report_challenge(request, id):

    if request.method == "POST":

        if "user_email" not in request.session:
            return JsonResponse({
                "error": "Login required"
            })

        try:

            user = User.objects.get(
                email=request.session["user_email"]
            )

            challenge = Challenge.objects.get(id=id)

            reason = request.POST.get("reason")

            Report.objects.create(
                user=user,
                challenge=challenge,
                reason=reason
            )

            return JsonResponse({
                "success": True
            })

        except:

            return JsonResponse({
                "error": "Failed"
            })

    return JsonResponse({
        "error": "Invalid request"
    })

# -------------------------
# API - REPORTS
# -------------------------
def get_reports(request):

    reports = Report.objects.all().order_by("-id")

    data = []

    for report in reports:

        data.append({
            "id": report.id,
            "challenge_id": report.challenge.id,
            "challenge_name": report.challenge.name,
            "days": report.challenge.days,
            "image": report.challenge.image,
            "reason": report.reason,
            "user": report.user.name
        })

    return JsonResponse(data, safe=False)


# -------------------------
# DELETE CHALLENGE
# -------------------------
def delete_challenge(request, id):

    try:

        challenge = Challenge.objects.get(id=id)
        trainer = challenge.trainer

        Activity.objects.create(
            trainer=trainer,
            message=f"Deleted challenge: {challenge.name}"
        )

        challenge.delete()

        return JsonResponse({
            "success": True
        })

    except:

        return JsonResponse({
            "error": "Challenge not found"
        })


# -------------------------
# DELETE REPORT
# -------------------------
def delete_report(request, id):

    try:

        report = Report.objects.get(id=id)

        report.delete()

        return JsonResponse({
            "success": True
        })

    except:

        return JsonResponse({
            "error": "Report not found"
        })
    

    # -------------------------
# ADMIN DASHBOARD STATS
# -------------------------
def admin_stats(request):

    total_users = User.objects.filter(role="user").count()

    total_trainers = Trainer.objects.count()

    total_challenges = Challenge.objects.count()

    total_reports = Report.objects.count()

    pending_trainers = Trainer.objects.filter(
        status="pending"
    )

    trainer_data = []

    for t in pending_trainers:

        trainer_data.append({
            "id": t.id,
            "name": t.user.name,
            "status": t.status
        })

    return JsonResponse({
        "users": total_users,
        "trainers": total_trainers,
        "challenges": total_challenges,
        "reports": total_reports,
        "pending_trainers": trainer_data
    })


# -------------------------
# TRAINER DASHBOARD STATS
# -------------------------
# -------------------------
# TRAINER STATS
# -------------------------
def trainer_stats(request):

    try:

        if "user_email" not in request.session:

            return JsonResponse({
                "error": "Login required"
            })

        user = User.objects.get(
            email=request.session["user_email"]
        )

        trainer = Trainer.objects.get(
            user=user
        )

        challenges = Challenge.objects.filter(
            trainer=trainer
        )

        challenge_count = challenges.count()

        # UNIQUE USERS
        joined_users = JoinChallenge.objects.filter(
                challenge__in=challenges
            ).values(
                "user"
            ).distinct().count()

        activities = Activity.objects.filter(
                trainer=trainer
            ).order_by(
                "-created_at"
            )[:5]

        activity_data = []

        for act in activities:

            activity_data.append({

                "message":
                    act.message,

                "time":
                    act.created_at.strftime(
                        "%d %b %Y"
                    )
            })

        return JsonResponse({

            "approved":
                str(trainer.status).lower().strip() == "approved",

            "challenge_count":
                challenge_count,

            "joined_users":
                joined_users,

            "activities":
                activity_data
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })


# -------------------------
# USER DASHBOARD STATS
# -------------------------
def user_stats(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        joined = JoinChallenge.objects.filter(
            user=user
        )

        joined_count = joined.count()

        # JOINED CHALLENGES
        challenge_names = []

        for j in joined:

            challenge_names.append(
                j.challenge.name
            )

        # USER RANK
        users = User.objects.filter(
            role="user"
        ).order_by("-streak")

        rank = 1

        for u in users:

            if u.id == user.id:
                break

            rank += 1

        return JsonResponse({

            "joined_count":
                joined_count,

            "streak":
                user.streak,

            "longest_streak":
                user.longest_streak,

            "rank":
                f"#{rank}",

            "goal":
                "Fitness",

            "challenges":
                challenge_names
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })
    
    # -------------------------
# TRAINER CHALLENGES
# -------------------------
def trainer_challenges_api(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        trainer = Trainer.objects.get(user=user)

        challenges = Challenge.objects.filter(
            trainer=trainer
        ).order_by("-id")

        data = []

        for ch in challenges:

            joined_count = JoinChallenge.objects.filter(
                challenge=ch
            ).count()

            data.append({
                "id": ch.id,
                "name": ch.name,
                "days": ch.days,
                "image": ch.image,
                "category": ch.category,
                "joined": joined_count
            })

        return JsonResponse(data, safe=False)

    except:

        return JsonResponse([], safe=False)


# -------------------------
# EDIT CHALLENGE
# -------------------------
def edit_challenge(request, id):

    if request.method == "POST":

        try:

            challenge = Challenge.objects.get(id=id)

            challenge.name = request.POST.get("name")
            challenge.days = request.POST.get("days")
            challenge.category = request.POST.get("category")

            challenge.save()

            Activity.objects.create(
                trainer=challenge.trainer,
                message=f"Updated challenge: {challenge.name}"
            )

            return JsonResponse({
                "success": True
            })

        except:

            return JsonResponse({
                "error": "Failed"
            })

    return JsonResponse({
        "error": "Invalid request"
    })

# -------------------------
# TRAINER LEADERBOARD
# -------------------------
def trainer_leaderboard_api(request):

    trainers = Trainer.objects.all()

    data = []

    for trainer in trainers:

        total_challenges = Challenge.objects.filter(
            trainer=trainer
        ).count()

        total_joined = JoinChallenge.objects.filter(
            challenge__trainer=trainer
        ).count()

        data.append({
            "name": trainer.user.name,
            "challenges": total_challenges,
            "joined": total_joined
        })

    # SORT BY CHALLENGE COUNT
    data = sorted(
        data,
        key=lambda x: x["challenges"],
        reverse=True
    )

    return JsonResponse(data, safe=False)


def trainer_challenge_detail(request):
    return render(
        request,
        "trainer/challenge-detail.html"
    )

# -------------------------
# ADMIN TRAINER REQUESTS
# -------------------------
def trainer_requests_api(request):

    trainers = Trainer.objects.all()

    data = []

    accepted = 0
    rejected = 0
    pending = 0

    for t in trainers:

        if t.status == "approved":
            accepted += 1

        elif t.status == "rejected":
            rejected += 1

        else:
            pending += 1

        data.append({
            "id": t.id,
            "name": t.user.name,
            "certificate": t.certificate,
            "status": t.status
        })

    return JsonResponse({
        "trainers": data,
        "accepted": accepted,
        "rejected": rejected,
        "pending": pending
    })

# -------------------------
# APPROVE TRAINER
# -------------------------
def approve_trainer(request, id):

    try:

        trainer = Trainer.objects.get(id=id)

        trainer.status = "approved"

        trainer.save()

        return JsonResponse({
            "success": True
        })

    except:

        return JsonResponse({
            "error": "Trainer not found"
        })
    
    # -------------------------
# REJECT TRAINER
# -------------------------
def reject_trainer(request, id):

    try:

        trainer = Trainer.objects.get(id=id)

        trainer.status = "rejected"

        trainer.save()

        return JsonResponse({
            "success": True
        })

    except:

        return JsonResponse({
            "error": "Trainer not found"
        })
    

# -------------------------
# ADMIN DASHBOARD STATS
# -------------------------
def admin_stats(request):

    total_users = User.objects.filter(
        role="user"
    ).count()

    total_trainers = Trainer.objects.count()

    approved_trainers = Trainer.objects.filter(
        status="approved"
    ).count()

    pending_trainers = Trainer.objects.filter(
        status="pending"
    ).count()

    total_challenges = Challenge.objects.count()

    total_reports = Report.objects.count()

    return JsonResponse({

        "users": total_users,

        "trainers": total_trainers,

        "approved_trainers": approved_trainers,

        "pending_trainers": pending_trainers,

        "challenges": total_challenges,

        "reports": total_reports
    })

# -------------------------
# TRAINER PROFILE API
# -------------------------
def trainer_profile_api(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        trainer = Trainer.objects.get(
            user=user
        )

        return JsonResponse({

            "name": user.name,

            "email": user.email,

            "specialization":
                user.specialization or "",

            "experience":
                user.experience or "",

            "status":
                trainer.status,

            "certificate":
                trainer.certificate
        })

    except:

        return JsonResponse({
            "error": "Trainer not found"
        })
    
# -------------------------
# UPDATE TRAINER PROFILE
# -------------------------
def update_trainer_profile(request):

    if request.method == "POST":

        try:

            user = User.objects.get(
                email=request.session["user_email"]
            )

            user.name = request.POST.get("name")

            user.email = request.POST.get("email")

            user.specialization = request.POST.get(
                    "specialization"
                )

            user.experience = request.POST.get(
                    "experience"
                )

            user.save()

            # IMPORTANT
            request.session[
                "user_email"
            ] = user.email

            return JsonResponse({
                "success": True
            })

        except:

            return JsonResponse({
                "error": "Something went wrong"
            })

    return JsonResponse({
        "error": "Invalid request"
    })

def reupload_certificate(request):

    if request.method == "POST":

        try:

            user = User.objects.get(
                email=request.session["user_email"]
            )

            trainer = Trainer.objects.get(
                user=user
            )

            certificate = request.POST.get(
                "certificate"
            )

            trainer.certificate = certificate

            trainer.status = "pending"

            trainer.save()

            return JsonResponse({
                "success": True
            })

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            })

    return JsonResponse({
        "error": "Invalid request"
    })

# -------------------------
# PUBLIC CHALLENGES
# -------------------------
def public_challenges(request):

    challenges = Challenge.objects.filter(
        trainer__status="approved"
    ).order_by("-id")[:6]

    data = []

    for ch in challenges:

        data.append({

            "id": ch.id,

            "name": ch.name,

            "days": ch.days,

            "image": ch.image,

            "category": ch.category,

            "trainer":
                ch.trainer.user.name
        })

    return JsonResponse(data, safe=False)

# -------------------------
# COMPLETE CHALLENGE
# -------------------------
def complete_challenge(request, challenge_id):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        join = JoinChallenge.objects.get(
            user=user,
            challenge_id=challenge_id
        )

        # ALREADY COMPLETED TODAY
        today = date.today()

        if join.completed_date == today:

            return JsonResponse({
                "message":
                "Already completed today",
                "streak":
                user.streak
            })

        # UPDATE JOIN
        join.completed_date = today
        join.save()

        # FIRST TIME
        if not user.last_streak_date:

            user.streak = 1

        else:

            diff = (
                today -
                user.last_streak_date
            ).days

            # CONTINUE STREAK
            if diff == 1:

                user.streak += 1

            # SAME DAY
            elif diff == 0:

                pass

            # MISSED DAY
            else:

                user.streak = 1

        # UPDATE LONGEST
        if user.streak > user.longest_streak:

            user.longest_streak = user.streak

        # SAVE DATE
        user.last_streak_date = today

        user.save()

        return JsonResponse({

            "success": True,

            "streak":
                user.streak,

            "longest":
                user.longest_streak
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })
    

# -------------------------
# USER LEADERBOARD PAGE
# -------------------------
def user_leaderboard_page(request):

    return render(
        request,
        "user/leaderboard.html"
    )

# -------------------------
# USER LEADERBOARD
# -------------------------
def user_leaderboard(request):

    users = User.objects.filter(
        role="user"
    ).order_by("-streak")

    data = []

    for user in users:

        joined_count = JoinChallenge.objects.filter(
            user=user
        ).count()

        data.append({

            "name":
                user.name,

            "streak":
                user.streak,

            "longest":
                user.longest_streak,

            "joined":
                joined_count
        })

    return JsonResponse(
        data,
        safe=False
    )

# -------------------------
# ADD WEIGHT
# -------------------------
def add_weight(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    if request.method != "POST":

        return JsonResponse({
            "error": "POST required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        weight = request.POST.get(
            "weight"
        )

        if not weight:

            return JsonResponse({
                "error": "Weight missing"
            })

        WeightLog.objects.create(
            user=user,
            weight=float(weight)
        )

        return JsonResponse({
            "success": True
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })


# -------------------------
# WEIGHT HISTORY
# -------------------------
def weight_history(request):

    if "user_email" not in request.session:

        return JsonResponse([], safe=False)

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        logs = WeightLog.objects.filter(
            user=user
        ).order_by("logged_date", "id")

        data = []

        for log in logs:

            data.append({

                "date":
                    log.logged_date.strftime(
                        "%d %b"
                    ),

                "weight":
                    float(log.weight)
            })

        return JsonResponse(
            data,
            safe=False
        )

    except:

        return JsonResponse(
            [],
            safe=False
        )
    

# -------------------------
# ADD CALORIES
# -------------------------
def add_calories(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    if request.method != "POST":

        return JsonResponse({
            "error": "POST required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        food_name = request.POST.get(
            "food_name"
        )

        calories = request.POST.get(
            "calories"
        )

        if not food_name or not calories:

            return JsonResponse({
                "error": "Missing data"
            })

        CalorieLog.objects.create(

            user=user,

            food_name=food_name,

            calories=int(calories)
        )

        return JsonResponse({
            "success": True
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })


# -------------------------
# CALORIE STATS
# -------------------------
from django.utils import timezone
from datetime import timedelta

def calorie_stats(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "today": 0,
            "week": 0,
            "month": 0,
            "entries": []
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        today = timezone.now().date()

        week_ago = today - timedelta(days=7)

        month_start = today.replace(day=1)

        # TODAY
        today_logs = CalorieLog.objects.filter(
            user=user,
            created_at__date=today
        )

        today_total = sum(
            log.calories for log in today_logs
        )

        # WEEK
        week_logs = CalorieLog.objects.filter(
            user=user,
            created_at__date__gte=week_ago
        )

        week_total = sum(
            log.calories for log in week_logs
        )

        # MONTH
        month_logs = CalorieLog.objects.filter(
            user=user,
            created_at__date__gte=month_start
        )

        month_total = sum(
            log.calories for log in month_logs
        )

        entries = []

        for log in today_logs:

            entries.append({

                "food": log.food_name,

                "calories": log.calories
            })

        return JsonResponse({

            "today": today_total,

            "week": week_total,

            "month": month_total,

            "entries": entries
        })

    except Exception as e:

        return JsonResponse({

            "today": 0,

            "week": 0,

            "month": 0,

            "entries": [],

            "error": str(e)
        })
    
# -------------------------
# USER PROFILE API
# -------------------------
def user_profile_api(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        return JsonResponse({

            "name": user.name,

            "email": user.email,

            "goal":
                getattr(
                    user,
                    "goal",
                    "Weight Loss"
                )
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })


# -------------------------
# UPDATE USER PROFILE
# -------------------------
def update_user_profile(request):

    if "user_email" not in request.session:

        return JsonResponse({
            "error": "Login required"
        })

    if request.method != "POST":

        return JsonResponse({
            "error": "POST required"
        })

    try:

        user = User.objects.get(
            email=request.session["user_email"]
        )

        user.name = request.POST.get(
            "name"
        )

        goal = request.POST.get(
            "goal"
        )

        user.goal = goal

        user.save()

        return JsonResponse({
            "success": True
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })
    
# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):

    request.session.flush()

    return redirect('/login/')

# -------------------------
# GET APPROVED TRAINERS
# -------------------------
def approved_trainers(request):

    trainers = Trainer.objects.filter(
        status="approved"
    )

    data = []

    for trainer in trainers:

        challenge_count = Challenge.objects.filter(
            trainer=trainer
        ).count()

        data.append({

            "id": trainer.id,

            "name": trainer.user.name,

            "specialization":
                trainer.user.specialization,

            "experience":
                trainer.user.experience,

            "challenge_count":
                challenge_count,

            "image":
                "https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=400&auto=format&fit=crop"
        })

    return JsonResponse(
        data,
        safe=False
    )

# -------------------------
# TRAINER DETAIL API
# -------------------------
def trainer_detail_api(request, id):

    try:

        trainer = Trainer.objects.get(
            id=id,
            status="approved"
        )

        challenges = Challenge.objects.filter(
                trainer=trainer
            )

        challenge_data = []

        for ch in challenges:

            challenge_data.append({

                "id": ch.id,

                "name": ch.name
            })

        data = {

            "id": trainer.id,

            "name": trainer.user.name,

            "specialization":
                trainer.user.specialization,

            "experience":
                trainer.user.experience,

            "email":
                trainer.user.email,

            "challenges":
                challenge_data,

            "image":
                "https://images.unsplash.com/photo-1599058917212-d750089bc07e?q=80&w=400&auto=format&fit=crop"
        }

        return JsonResponse(data)

    except:

        return JsonResponse({
            "error": "Trainer not found"
        })
    
# -------------------------
# UPDATE PROGRESS
# -------------------------
# -------------------------
# UPDATE CHALLENGE PROGRESS
# -------------------------
def update_progress(request, id):

    if request.method != "POST":

        return JsonResponse({
            "error": "POST required"
        })

    try:

        if "user_email" not in request.session:

            return JsonResponse({
                "error": "Login required"
            })

        user = User.objects.get(
            email=request.session["user_email"]
        )

        challenge = Challenge.objects.get(
            id=id
        )

        joined = JoinChallenge.objects.get(
            challenge_id=id,
            user=user
        )

        progress = int(
            request.POST.get("progress")
        )

        if progress < 0:
            progress = 0

        if progress > 100:
            progress = 100

        joined.progress = progress

        # AUTO COMPLETE
        if progress == 100:

            joined.completed_date = timezone.now().date()

        joined.save()

        return JsonResponse({

            "success": True,

            "progress": joined.progress
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        })
    
# -------------------------
# CHALLENGE PROGRESS
# -------------------------
# -------------------------
# GET CHALLENGE PROGRESS
# -------------------------
def challenge_progress(request, id):

    try:

        if "user_email" not in request.session:

            return JsonResponse({
                "progress": 0
            })

        user = User.objects.get(
            email=request.session["user_email"]
        )

        challenge = Challenge.objects.get(
            id=id
        )

        joined = JoinChallenge.objects.get(
            user=user,
            challenge=challenge
        )

        return JsonResponse({

            "progress": joined.progress
        })

    except Exception as e:

        return JsonResponse({

            "progress": 0,

            "error": str(e)
        })
    
# -------------------------
# USER PROGRESS GRAPH
# -------------------------
def user_progress(request):

    try:

        if "user_email" not in request.session:

            return JsonResponse(
                [],
                safe=False
            )

        user = User.objects.get(
            email=request.session["user_email"]
        )

        joined = JoinChallenge.objects.filter(
            user=user
        )

        data = []

        for item in joined:

            data.append({

                "name":
                    item.challenge.name,

                "progress":
                    item.progress
            })

        return JsonResponse(
            data,
            safe=False
        )

    except Exception as e:

        return JsonResponse({

            "error": str(e)
        })