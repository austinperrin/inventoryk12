from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status  # type: ignore[import-untyped]
from rest_framework.test import APITestCase  # type: ignore[import-untyped]
from rest_framework_simplejwt.token_blacklist.models import (  # type: ignore[import-untyped]
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore[import-untyped]


class AuthApiTests(APITestCase):
    def setUp(self) -> None:
        self.user_model = get_user_model()
        self.password = "super-secret-pass"
        self.user = self.user_model.objects.create_user(
            email="teacher@example.com",
            password=self.password,
            first_name="Taylor",
            last_name="Teacher",
        )

    def _auth_headers(self, user=None) -> dict[str, str]:
        actor = user or self.user
        refresh = RefreshToken.for_user(actor)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    def test_login_returns_tokens_and_user_summary(self) -> None:
        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.user.email, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["email"], self.user.email)
        self.assertEqual(response.data["user"]["full_name"], "Taylor Teacher")

    def test_login_rejects_invalid_credentials(self) -> None:
        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": self.user.email, "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"].code, "no_active_account")

    def test_me_requires_authentication(self) -> None:
        response = self.client.get("/api/v1/auth/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_user_roles(self) -> None:
        role = Group.objects.create(name="teacher")
        self.user.groups.add(role)

        response = self.client.get("/api/v1/auth/me/", **self._auth_headers())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["roles"], ["teacher"])

    def test_refresh_issues_new_access_token(self) -> None:
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            "/api/v1/auth/refresh/",
            {"refresh": str(refresh)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_logout_blacklists_refresh_token(self) -> None:
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            "/api/v1/auth/logout/",
            {"refresh": str(refresh)},
            format="json",
            **self._auth_headers(),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(BlacklistedToken.objects.filter(token__jti=refresh["jti"]).exists())

    def test_rbac_check_forbidden_for_non_elevated_role(self) -> None:
        role = Group.objects.create(name="student")
        self.user.groups.add(role)

        response = self.client.get("/api/v1/auth/rbac-check/", **self._auth_headers())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rbac_check_allows_elevated_role(self) -> None:
        role = Group.objects.create(name="district_admin")
        self.user.groups.add(role)

        response = self.client.get("/api/v1/auth/rbac-check/", **self._auth_headers())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "allowed")
