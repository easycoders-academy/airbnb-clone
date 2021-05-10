from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/vk/", views.vk_login, name="vk-login"),
    path("login/vk/callback/", views.vk_callback, name="vk-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:key>/", views.complete_verification, name="complete-verification"
    ),
    path("<int:pk>/", views.UserProfileView.as_view(), name="profile"),
    path("switch-hosting/", views.switch_hosting, name="switch-hosting"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update"),
    path("update-password/", views.UpdatePasswordView.as_view(), name="password"),
]
