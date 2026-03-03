from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):  # type: ignore[misc]
    def authenticate(self, request: Request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token

        raw_cookie_token = request.COOKIES.get(settings.AUTH_ACCESS_COOKIE_NAME)
        if not raw_cookie_token:
            return None

        validated_token = self.get_validated_token(raw_cookie_token)
        self._enforce_csrf(request)
        return self.get_user(validated_token), validated_token

    def _enforce_csrf(self, request: Request) -> None:
        check = CSRFCheck(lambda req: None)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")
