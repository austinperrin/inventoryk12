from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.response import Response  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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


def _set_auth_cookies(response: Response, access_token: str, refresh_token: str | None = None) -> None:
    _set_auth_cookie(response, settings.AUTH_ACCESS_COOKIE_NAME, access_token, settings.AUTH_ACCESS_COOKIE_MAX_AGE)
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


class LoginView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        response = Response({"user": UserSummarySerializer(user).data}, status=status.HTTP_200_OK)
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
            response = Response({"detail": "Refresh token missing."}, status=status.HTTP_401_UNAUTHORIZED)
            _clear_auth_cookies(response)
            return response

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            response = Response({"detail": "Refresh token invalid."}, status=status.HTTP_401_UNAUTHORIZED)
            _clear_auth_cookies(response)
            return response

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
            return Response({"authenticated": True, "user": UserSummarySerializer(request.user).data})
        return Response({"authenticated": False, "user": None})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class MeView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response({"user": UserSummarySerializer(request.user).data})
