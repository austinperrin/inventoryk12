from django.urls import path

from .views import (
    ChangePasswordView,
    CsrfView,
    ForgotPasswordView,
    LoginView,
    LogoutView,
    MeView,
    ReauthView,
    RefreshView,
    ResetPasswordView,
    SessionView,
)

urlpatterns = [
    path("csrf/", CsrfView.as_view(), name="auth-csrf"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="auth-forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="auth-reset-password"),
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"),
    path("re-auth/", ReauthView.as_view(), name="auth-re-auth"),
    path("refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("session/", SessionView.as_view(), name="auth-session"),
    path("me/", MeView.as_view(), name="auth-me"),
]
