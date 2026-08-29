from django.urls import path
from . import views

urlpatterns = [

    # -------------------------
    # HOME
    # -------------------------
    path('', views.home),

    # -------------------------
    # SIGNUP
    # -------------------------
    path('signup1/', views.signup1),
    path('signup2/', views.signup2),
    path('signup-user/', views.signup_user),
    path('signup-trainer/', views.signup_trainer),
    path('signup/', views.signup),

    # -------------------------
    # LOGIN
    # -------------------------
    path('login/', views.login_view),
    path('login-user/', views.login_user),

    # -------------------------
    # USER ROUTES
    # -------------------------
    path('user/dashboard/', views.user_dashboard),
    path('user/challenges/', views.user_challenges),
    path('user/challenge-detail/', views.user_challenge_detail),
    path('user/profile/', views.user_profile),
    path('user/help/', views.user_help),
   path('user/leaderboard/', views.user_leaderboard_page),
    path('user/trainers/', views.user_trainers),
    path('user/trainer-detail/', views.user_trainer_detail),
    path('user/calories/', views.user_calories),

    # -------------------------
    # TRAINER ROUTES
    # -------------------------
    path('trainer/dashboard/', views.trainer_dashboard),
    path('trainer/challenges/', views.trainer_challenges),
    path('trainer/create-challenge/', views.create_challenge),
    path('trainer/leaderboard/', views.trainer_leaderboard),
    path('trainer/profile/', views.trainer_profile),
    path('trainer/help/', views.trainer_help),

    # -------------------------
    # ADMIN ROUTES
    # -------------------------
    path('admin/dashboard/', views.admin_dashboard),
    path('admin/manage-challenges/', views.admin_manage_challenges),
    path('admin/reports/', views.admin_reports),
    path('admin/certificate/', views.admin_certificate),

    path('api/challenges/', views.get_challenges),

    path('api/challenge/<int:id>/', views.get_single_challenge),

path('api/join-challenge/<int:id>/', views.join_challenge),

path('api/report-challenge/<int:id>/', views.report_challenge),

path('api/reports/', views.get_reports),

path('api/delete-challenge/<int:id>/', views.delete_challenge),

path('api/delete-report/<int:id>/', views.delete_report),

path('api/admin-stats/', views.admin_stats),

path('api/trainer-stats/', views.trainer_stats),

path('api/user-stats/', views.user_stats),

path('api/trainer-challenges/', views.trainer_challenges_api),

path('api/edit-challenge/<int:id>/', views.edit_challenge),

path(
    'api/trainer-leaderboard/',
    views.trainer_leaderboard_api
),

path(
    'trainer/challenge-detail/',
    views.trainer_challenge_detail
),

path(
    'api/trainer-requests/',
    views.trainer_requests_api
),

path(
    'api/approve-trainer/<int:id>/',
    views.approve_trainer
),

path(
    'api/reject-trainer/<int:id>/',
    views.reject_trainer
),

path(
    'api/admin-stats/',
    views.admin_stats
),

path(
    'api/create-challenge/',
    views.create_challenge_api
),

path(
    'api/trainer-profile/',
    views.trainer_profile_api
),

path(
    'api/update-trainer-profile/',
    views.update_trainer_profile
),

path(
    'api/reupload-certificate/',
    views.reupload_certificate
),

path(
    'api/public-challenges/',
    views.public_challenges
),

path(
    'api/complete-challenge/<int:challenge_id>/',
    views.complete_challenge
),

path(
    'api/user-leaderboard/',
    views.user_leaderboard
),

path(
    'api/add-weight/',
    views.add_weight
),

path(
    'api/weight-history/',
    views.weight_history
),

path(
    'api/add-calories/',
    views.add_calories
),

path(
    'api/calorie-stats/',
    views.calorie_stats
),

path(
    'api/user-profile/',
    views.user_profile_api
),

path(
    'api/update-user-profile/',
    views.update_user_profile
),

path(
    'logout/',
    views.logout_view
),

path(
    'api/approved-trainers/',
    views.approved_trainers
),

path(
    'api/trainer-detail/<int:id>/',
    views.trainer_detail_api
),

path(
    'api/update-progress/<int:id>/',
    views.update_progress
),

path(
    'api/challenge-progress/<int:id>/',
    views.challenge_progress
),

path(
    'api/user-progress/',
    views.user_progress
),
    # -------------------------
    # APPROVAL
    # -------------------------
    path('approve-trainer/<int:id>/', views.approve_trainer),
]