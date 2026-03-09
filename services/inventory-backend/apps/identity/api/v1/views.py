from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.response import Response  # type: ignore[import-untyped]
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView  # type: ignore[import-untyped]
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.identity.models import MfaPolicy
from apps.identity.services import (
    add_session_claims,
    issue_mfa_challenge,
    issue_mfa_cookie_value,
    issue_reauth_cookie_value,
    mfa_policy_summary,
    requires_mfa_for_user,
    resolve_user_access,
    validate_session_window,
    verify_mfa_challenge,
)
from apps.identity.services.session_security import SESSION_STARTED_AT_CLAIM

from .permissions import HasEffectiveAccess, IsSystemAdminOrSuperuser, RequiresPrivilegedStepUp
from .serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    MfaChallengeSerializer,
    MfaPolicySerializer,
    MfaPolicyUpdateSerializer,
    MfaVerifySerializer,
    ReauthSerializer,
    ResetPasswordSerializer,
    UserSummarySerializer,
)

User = get_user_model()
SESSION_VERSION_CLAIM = "ik12_session_version"


def _set_auth_cookie(response: Response, name: str, value: str, max_age: int) -> None:
    response.set_cookie(
        key=name,
        value=value,
        max_age=max_age,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )


def _set_auth_cookies(
    response: Response, access_token: str, refresh_token: str | None = None
) -> None:
    _set_auth_cookie(
        response,
        settings.AUTH_ACCESS_COOKIE_NAME,
        access_token,
        settings.AUTH_ACCESS_COOKIE_MAX_AGE,
    )
    if refresh_token is not None:
        _set_auth_cookie(
            response,
            settings.AUTH_REFRESH_COOKIE_NAME,
            refresh_token,
            settings.AUTH_REFRESH_COOKIE_MAX_AGE,
        )


def _set_reauth_cookie(response: Response, value: str) -> None:
    _set_auth_cookie(
        response,
        settings.AUTH_REAUTH_COOKIE_NAME,
        value,
        settings.AUTH_REAUTH_WINDOW_SECONDS,
    )


def _set_mfa_cookie(response: Response, value: str) -> None:
    _set_auth_cookie(
        response,
        settings.AUTH_MFA_COOKIE_NAME,
        value,
        settings.AUTH_MFA_RECENT_WINDOW_SECONDS,
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        settings.AUTH_ACCESS_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
    response.delete_cookie(
        settings.AUTH_REFRESH_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
    response.delete_cookie(
        settings.AUTH_REAUTH_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )
    response.delete_cookie(
        settings.AUTH_MFA_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
        samesite=settings.AUTH_COOKIE_SAMESITE,
    )


def _session_policy_payload() -> dict[str, int]:
    return {
        "idle_timeout_seconds": int(settings.AUTH_SESSION_IDLE_TIMEOUT_SECONDS),
        "absolute_lifetime_seconds": int(settings.AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS),
    }


class LoginView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "auth_login"

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.verified_at is None:
            user.verified_at = timezone.now()
            user.save(update_fields=["verified_at"])

        now = timezone.now()
        refresh = RefreshToken.for_user(user)
        refresh[SESSION_VERSION_CLAIM] = int(user.auth_session_version)
        add_session_claims(refresh, now=now)
        response = Response(
            {
                "user": UserSummarySerializer(user).data,
                "access": resolve_user_access(user),
                "session_policy": _session_policy_payload(),
            },
            status=status.HTTP_200_OK,
        )
        _set_auth_cookies(response, str(refresh.access_token), str(refresh))
        get_token(request)
        response["Cache-Control"] = "no-store"
        return response


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        get_token(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RefreshView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE_NAME)
        if not refresh_token:
            response = Response(
                {"detail": "Refresh token missing."}, status=status.HTTP_401_UNAUTHORIZED
            )
            _clear_auth_cookies(response)
            return response

        try:
            parsed_refresh_token = RefreshToken(refresh_token)
        except Exception:
            response = Response(
                {"detail": "Refresh token invalid."}, status=status.HTTP_401_UNAUTHORIZED
            )
            _clear_auth_cookies(response)
            return response

        token_user_id_raw = parsed_refresh_token.payload.get("user_id")
        if token_user_id_raw is None:
            response = Response(
                {"detail": "Session has been revoked."}, status=status.HTTP_401_UNAUTHORIZED
            )
            _clear_auth_cookies(response)
            return response
        token_user_id = str(token_user_id_raw)
        token_session_version = int(parsed_refresh_token.payload.get(SESSION_VERSION_CLAIM, 1))
        token_user = User.objects.filter(pk=token_user_id, is_active=True).first()
        if not token_user or int(token_user.auth_session_version) != token_session_version:
            response = Response(
                {"detail": "Session has been revoked."}, status=status.HTTP_401_UNAUTHORIZED
            )
            _clear_auth_cookies(response)
            return response

        is_valid_session, failure_reason = validate_session_window(
            parsed_refresh_token,
            now=timezone.now(),
        )
        if not is_valid_session:
            detail = "Session expired. Please sign in again."
            if failure_reason == "session_idle_timeout":
                detail = "Session idle timeout exceeded. Please sign in again."
            elif failure_reason == "session_absolute_timeout":
                detail = "Session absolute lifetime exceeded. Please sign in again."
            response = Response({"detail": detail}, status=status.HTTP_401_UNAUTHORIZED)
            _clear_auth_cookies(response)
            return response

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            response = Response(
                {"detail": "Refresh token invalid."}, status=status.HTTP_401_UNAUTHORIZED
            )
            _clear_auth_cookies(response)
            return response

        rotated_refresh_token = serializer.validated_data.get("refresh")
        if rotated_refresh_token:
            next_refresh_token = RefreshToken(rotated_refresh_token)
            next_refresh_token[SESSION_VERSION_CLAIM] = parsed_refresh_token.payload.get(
                SESSION_VERSION_CLAIM,
                1,
            )
            next_refresh_token[SESSION_STARTED_AT_CLAIM] = parsed_refresh_token.payload.get(
                SESSION_STARTED_AT_CLAIM,
                int(timezone.now().timestamp()),
            )
            add_session_claims(next_refresh_token, now=timezone.now())
            serializer.validated_data["refresh"] = str(next_refresh_token)
            serializer.validated_data["access"] = str(next_refresh_token.access_token)

        response = Response(status=status.HTTP_200_OK)
        _set_auth_cookies(
            response,
            serializer.validated_data["access"],
            serializer.validated_data.get("refresh"),
        )
        get_token(request)
        response["Cache-Control"] = "no-store"
        return response


class LogoutView(APIView):  # type: ignore[misc]
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE_NAME)
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass

        response = Response(status=status.HTTP_200_OK)
        _clear_auth_cookies(response)
        return response


class ForgotPasswordView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email, is_active=True).first()
        if user and user.has_usable_password():
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            send_mail(
                subject="InventoryK12 password reset request",
                message=(
                    "A password reset was requested for your account.\n\n"
                    f"uid={uid}\n"
                    f"token={token}\n\n"
                    "If you did not request this, contact your administrator."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ResetPasswordView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["new_password"])
        user.require_password_reset = False
        if user.verified_at is None:
            user.verified_at = timezone.now()
        user.save(update_fields=["password", "require_password_reset", "verified_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.require_password_reset = False
        request.user.save(update_fields=["password", "require_password_reset"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReauthView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = ReauthSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        _set_reauth_cookie(response, issue_reauth_cookie_value(request.user))
        return response


class MfaChallengeView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        if not requires_mfa_for_user(request.user):
            return Response({"detail": "MFA is not required for this account."})

        serializer = MfaChallengeSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        challenge_id = issue_mfa_challenge(request.user)
        return Response({"challenge_id": challenge_id}, status=status.HTTP_200_OK)


class MfaVerifyView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = MfaVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_valid = verify_mfa_challenge(
            request.user,
            serializer.validated_data["challenge_id"],
            serializer.validated_data["code"],
        )
        if not is_valid:
            return Response(
                {"detail": "Invalid or expired MFA challenge."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response(status=status.HTTP_204_NO_CONTENT)
        _set_mfa_cookie(response, issue_mfa_cookie_value(request.user))
        return response


class MfaPolicyView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, IsSystemAdminOrSuperuser]

    def get(self, request: Request) -> Response:
        serializer = MfaPolicySerializer(mfa_policy_summary())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        serializer = MfaPolicyUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        policy = MfaPolicy.objects.get_or_create(policy_key="default")[0]
        data = serializer.validated_data
        if "enforce_for_all" in data:
            policy.enforce_for_all = bool(data["enforce_for_all"])
        if "allow_user_opt_in" in data:
            policy.allow_user_opt_in = bool(data["allow_user_opt_in"])
        policy.save()

        if "enforced_role_names" in data:
            roles = Group.objects.filter(name__in=data["enforced_role_names"])
            policy.enforced_roles.set(roles)

        return Response(MfaPolicySerializer(mfa_policy_summary()).data, status=status.HTTP_200_OK)


class PrivilegedReviewHookView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, RequiresPrivilegedStepUp]

    def get(self, request: Request) -> Response:
        return Response(
            {"detail": "Privileged step-up requirement satisfied."},
            status=status.HTTP_200_OK,
        )


class SessionReviewView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, RequiresPrivilegedStepUp]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "auth_session_version": int(request.user.auth_session_version),
                "reauth_window_seconds": int(settings.AUTH_REAUTH_WINDOW_SECONDS),
                "mfa_recent_window_seconds": int(settings.AUTH_MFA_RECENT_WINDOW_SECONDS),
                "mfa_required_for_user": bool(requires_mfa_for_user(request.user)),
            },
            status=status.HTTP_200_OK,
        )


class RevokeAllSessionsView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, RequiresPrivilegedStepUp]

    def post(self, request: Request) -> Response:
        request.user.auth_session_version = int(request.user.auth_session_version) + 1
        request.user.save(update_fields=["auth_session_version"])
        response = Response(status=status.HTTP_204_NO_CONTENT)
        _clear_auth_cookies(response)
        return response


@method_decorator(ensure_csrf_cookie, name="dispatch")
class SessionView(APIView):  # type: ignore[misc]
    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        if request.user.is_authenticated:
            return Response(
                {
                    "authenticated": True,
                    "user": UserSummarySerializer(request.user).data,
                    "access": resolve_user_access(request.user),
                    "session_policy": _session_policy_payload(),
                }
            )
        return Response({"authenticated": False, "user": None})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class MeView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, HasEffectiveAccess]

    def get(self, request: Request) -> Response:
        return Response(
            {
                "user": UserSummarySerializer(request.user).data,
                "access": resolve_user_access(request.user),
            }
        )
