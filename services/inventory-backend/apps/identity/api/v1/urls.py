from django.urls import path

from .views import LoginView, LogoutView, MeView, RbacCheckView, RefreshView

urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("me/", MeView.as_view(), name="auth-me"),
    path("rbac-check/", RbacCheckView.as_view(), name="auth-rbac-check"),
]
