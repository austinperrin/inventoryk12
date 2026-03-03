from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
API_PREFIX = f"{settings.APP_ENV_PATH_PREFIX}/api/v1"


def _csrf_client() -> APIClient:
    client = APIClient(enforce_csrf_checks=True)
    csrf_response = client.get(f"{API_PREFIX}/auth/csrf/")
    assert csrf_response.status_code == 204
    csrf_token = client.cookies["csrftoken"].value
    client.defaults["HTTP_X_CSRFTOKEN"] = csrf_token
    return client


def test_auth_csrf_endpoint_sets_cookie_without_authentication() -> None:
    client = APIClient(enforce_csrf_checks=True)

    response = client.get(f"{API_PREFIX}/auth/csrf/")

    assert response.status_code == 204
    assert "csrftoken" in client.cookies


def test_auth_session_reports_guest_without_authentication() -> None:
    client = APIClient(enforce_csrf_checks=True)

    response = client.get(f"{API_PREFIX}/auth/session/")

    assert response.status_code == 200
    assert response.data == {"authenticated": False, "user": None}


def test_auth_login_sets_cookie_backed_tokens_and_me_uses_them(db) -> None:
    user = User.objects.create_user(
        email="admin@example.com",
        password="ChangeMe123!",
        first_name="Ada",
        last_name="Lovelace",
    )
    client = _csrf_client()

    response = client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["user"]["email"] == user.email
    assert "ik12_access" in client.cookies
    assert "ik12_refresh" in client.cookies
    assert client.cookies["ik12_access"]["httponly"]
    assert client.cookies["ik12_refresh"]["httponly"]

    me_response = client.get(f"{API_PREFIX}/auth/me/")

    assert me_response.status_code == 200
    assert me_response.data["user"]["email"] == user.email


def test_auth_refresh_rotates_refresh_token(db) -> None:
    user = User.objects.create_user(
        email="refresh@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    login_response = client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )
    original_refresh = login_response.cookies["ik12_refresh"].value

    refresh_response = client.post(f"{API_PREFIX}/auth/refresh/", {}, format="json")

    assert refresh_response.status_code == 200
    assert client.cookies["ik12_refresh"].value != original_refresh
    assert client.cookies["ik12_access"].value


def test_auth_logout_clears_cookies_and_blacklists_refresh_token(db) -> None:
    user = User.objects.create_user(
        email="logout@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    logout_response = client.post(f"{API_PREFIX}/auth/logout/", {}, format="json")

    assert logout_response.status_code == 200
    assert logout_response.cookies["ik12_access"].value == ""
    assert logout_response.cookies["ik12_refresh"].value == ""

    refresh_response = client.post(f"{API_PREFIX}/auth/refresh/", {}, format="json")
    assert refresh_response.status_code == 401
