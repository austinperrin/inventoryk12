from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.utils import timezone
from rest_framework.test import APIClient

from apps.identity.models import RoleAssignment, UserLoginLock

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
    assert response.data["access"]["has_effective_access"] is False
    assert response.data["access"]["access_outcome"] == "no_access"
    assert response.data["access"]["no_access_reason"] == "no_effective_permissions"
    assert (
        response.data["access"]["no_access_message"]
        == "Your account is active but has no effective permissions assigned."
    )
    assert "ik12_access" in client.cookies
    assert "ik12_refresh" in client.cookies
    assert client.cookies["ik12_access"]["httponly"]
    assert client.cookies["ik12_refresh"]["httponly"]

    me_response = client.get(f"{API_PREFIX}/auth/me/")

    assert me_response.status_code == 403
    assert (
        me_response.data["detail"]
        == "Your account is active but has no effective permissions assigned."
    )


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


def test_auth_me_denies_guest_user() -> None:
    client = APIClient(enforce_csrf_checks=True)

    response = client.get(f"{API_PREFIX}/auth/me/")

    assert response.status_code == 401


def test_auth_login_reports_granted_access_from_active_role_assignment(db) -> None:
    user = User.objects.create_user(
        email="roles@example.com",
        password="ChangeMe123!",
    )
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    role = Group.objects.create(name="district_admin")
    role.permissions.add(view_group_permission)
    today = timezone.localdate()
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=today,
    )
    client = _csrf_client()

    response = client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    assert response.status_code == 200
    assert response.data["access"]["has_effective_access"] is True
    assert response.data["access"]["access_outcome"] == "granted"
    assert response.data["access"]["no_access_reason"] is None
    assert response.data["access"]["no_access_message"] is None
    assert response.data["access"]["is_verified"] is True
    assert "auth.view_group" in response.data["access"]["permissions"]

    me_response = client.get(f"{API_PREFIX}/auth/me/")
    assert me_response.status_code == 200
    assert me_response.data["user"]["email"] == user.email
    assert me_response.data["access"]["has_effective_access"] is True


def test_auth_session_reports_granted_access_from_direct_user_permission(db) -> None:
    user = User.objects.create_user(
        email="direct@example.com",
        password="ChangeMe123!",
    )
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    user.user_permissions.add(view_group_permission)
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")

    assert session_response.status_code == 200
    assert session_response.data["authenticated"] is True
    assert session_response.data["access"]["has_effective_access"] is True
    assert session_response.data["access"]["access_outcome"] == "granted"
    assert session_response.data["access"]["no_access_reason"] is None
    assert session_response.data["access"]["no_access_message"] is None
    assert "auth.view_group" in session_response.data["access"]["permissions"]


def test_auth_session_ignores_expired_role_assignments_for_access(db) -> None:
    user = User.objects.create_user(
        email="expired@example.com",
        password="ChangeMe123!",
    )
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    role = Group.objects.create(name="teacher")
    role.permissions.add(view_group_permission)
    today = timezone.localdate()
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=today - timedelta(days=2),
        ends_on=today - timedelta(days=1),
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")

    assert session_response.status_code == 200
    assert session_response.data["authenticated"] is True
    assert session_response.data["access"]["has_effective_access"] is False
    assert session_response.data["access"]["access_outcome"] == "no_access"
    assert session_response.data["access"]["no_access_reason"] == "no_effective_permissions"
    assert (
        session_response.data["access"]["no_access_message"]
        == "Your account is active but has no effective permissions assigned."
    )


def test_auth_session_reports_no_access_when_user_has_active_login_lock(db) -> None:
    user = User.objects.create_user(
        email="locked@example.com",
        password="ChangeMe123!",
    )
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    role = Group.objects.create(name="system_admin")
    role.permissions.add(view_group_permission)
    today = timezone.localdate()
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=today,
    )
    UserLoginLock.objects.create(
        user=user,
        reason="Your account is locked. Contact district support.",
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")
    me_response = client.get(f"{API_PREFIX}/auth/me/")

    assert session_response.status_code == 200
    assert session_response.data["access"]["has_effective_access"] is False
    assert session_response.data["access"]["no_access_reason"] == "login_locked"
    assert (
        session_response.data["access"]["no_access_message"]
        == "Your account is locked. Contact district support."
    )
    assert session_response.data["access"]["has_active_login_lock"] is True
    assert me_response.status_code == 403
    assert me_response.data["detail"] == "Your account is locked. Contact district support."
