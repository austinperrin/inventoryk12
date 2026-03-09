from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]

from apps.identity.services import (
    has_active_system_admin_role,
    has_recent_mfa_cookie,
    has_recent_reauth_cookie,
    requires_mfa_for_user,
    resolve_user_access,
)


class HasEffectiveAccess(BasePermission):
    message = "No effective access is available for this account."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        access = resolve_user_access(request.user)
        self.message = str(access.get("no_access_message") or self.message)
        return bool(access["has_effective_access"])


class RequiresRecentReauth(BasePermission):
    message = "Recent re-authentication is required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        reauth_cookie = request.COOKIES.get(settings.AUTH_REAUTH_COOKIE_NAME)
        return has_recent_reauth_cookie(reauth_cookie, request.user)


class RequiresRecentMfa(BasePermission):
    message = "Recent MFA verification is required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if not requires_mfa_for_user(request.user):
            return True

        mfa_cookie = request.COOKIES.get(settings.AUTH_MFA_COOKIE_NAME)
        return has_recent_mfa_cookie(mfa_cookie, request.user)


class RequiresPrivilegedStepUp(BasePermission):
    message = "Privileged action requires re-authentication."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        reauth_cookie = request.COOKIES.get(settings.AUTH_REAUTH_COOKIE_NAME)
        has_reauth = has_recent_reauth_cookie(reauth_cookie, request.user)
        if not has_reauth:
            return False

        if not requires_mfa_for_user(request.user):
            return True

        mfa_cookie = request.COOKIES.get(settings.AUTH_MFA_COOKIE_NAME)
        return has_recent_mfa_cookie(mfa_cookie, request.user)


class IsSystemAdminOrSuperuser(BasePermission):
    message = "System administrator privileges are required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        return bool(request.user.is_superuser or has_active_system_admin_role(request.user))
