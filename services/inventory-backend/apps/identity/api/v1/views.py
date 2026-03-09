from django.conf import settings
from django.middleware.csrf import get_token
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.response import Response  # type: ignore[import-untyped]
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView  # type: ignore[import-untyped]
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.identity.services import add_session_claims, resolve_user_access, validate_session_window
from apps.identity.services.session_security import SESSION_STARTED_AT_CLAIM

from .permissions import HasEffectiveAccess
from .serializers import LoginSerializer, UserSummarySerializer


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
