from datetime import timedelta

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.cache import cache
from django.test import override_settings
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from apps.identity.models import MfaPolicy, RoleAssignment, UserLoginLock
from apps.identity.services import has_recent_reauth_cookie

User = get_user_model()
API_PREFIX = f"{settings.APP_ENV_PATH_PREFIX}/api/v1"


@pytest.fixture(autouse=True)
def _clear_auth_throttle_cache():
    cache.clear()
    yield
    cache.clear()


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


def test_auth_login_is_rate_limited_after_threshold(db) -> None:
    cache.clear()
    user = User.objects.create_user(
        email="throttle@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()

    configured_rate = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["auth_login"]
    limit = int(str(configured_rate).split("/", maxsplit=1)[0])
    response = None
    for _ in range(limit):
        response = client.post(
            f"{API_PREFIX}/auth/login/",
            {"email": user.email, "password": "WrongPassword123!"},
            format="json",
        )
        assert response.status_code == 400

    response = client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "WrongPassword123!"},
        format="json",
    )

    assert response.status_code == 429
    cache.clear()


def test_auth_refresh_denies_when_idle_timeout_is_exceeded(db, monkeypatch) -> None:
    user = User.objects.create_user(
        email="idle-timeout@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    base_now = timezone.now()
    monkeypatch.setattr("apps.identity.api.v1.views.timezone.now", lambda: base_now)

    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    monkeypatch.setattr(
        "apps.identity.api.v1.views.timezone.now",
        lambda: base_now + timedelta(seconds=61),
    )
    with override_settings(
        AUTH_SESSION_IDLE_TIMEOUT_SECONDS=60,
        AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS=3600,
    ):
        refresh_response = client.post(f"{API_PREFIX}/auth/refresh/", {}, format="json")

    assert refresh_response.status_code == 401
    assert refresh_response.data["detail"] == "Session idle timeout exceeded. Please sign in again."
    assert refresh_response.cookies["ik12_access"].value == ""
    assert refresh_response.cookies["ik12_refresh"].value == ""


def test_auth_refresh_denies_when_absolute_lifetime_is_exceeded(db, monkeypatch) -> None:
    user = User.objects.create_user(
        email="absolute-timeout@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    base_now = timezone.now()
    monkeypatch.setattr("apps.identity.api.v1.views.timezone.now", lambda: base_now)

    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    monkeypatch.setattr(
        "apps.identity.api.v1.views.timezone.now",
        lambda: base_now + timedelta(seconds=121),
    )
    with override_settings(
        AUTH_SESSION_IDLE_TIMEOUT_SECONDS=3600,
        AUTH_SESSION_ABSOLUTE_LIFETIME_SECONDS=120,
    ):
        refresh_response = client.post(f"{API_PREFIX}/auth/refresh/", {}, format="json")

    assert refresh_response.status_code == 401
    assert (
        refresh_response.data["detail"]
        == "Session absolute lifetime exceeded. Please sign in again."
    )
    assert refresh_response.cookies["ik12_access"].value == ""
    assert refresh_response.cookies["ik12_refresh"].value == ""


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


def test_auth_session_reports_no_access_when_password_reset_is_required(db) -> None:
    user = User.objects.create_user(
        email="require-reset@example.com",
        password="ChangeMe123!",
        require_password_reset=True,
    )
    view_group_permission = Permission.objects.get(
        content_type__app_label="auth",
        codename="view_group",
    )
    role = Group.objects.create(name="teacher-reset")
    role.permissions.add(view_group_permission)
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=timezone.localdate(),
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
    assert session_response.data["access"]["no_access_reason"] == "require_password_reset"
    assert (
        session_response.data["access"]["no_access_message"]
        == "You must reset your password before continuing."
    )
    assert me_response.status_code == 403
    assert me_response.data["detail"] == "You must reset your password before continuing."


def test_auth_forgot_password_returns_204_and_sends_email_for_known_user(db) -> None:
    user = User.objects.create_user(
        email="forgot@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()

    response = client.post(
        f"{API_PREFIX}/auth/forgot-password/",
        {"email": user.email},
        format="json",
    )

    assert response.status_code == 204
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to


def test_auth_forgot_password_returns_204_for_unknown_user_without_email(db) -> None:
    client = _csrf_client()
    mail.outbox.clear()

    response = client.post(
        f"{API_PREFIX}/auth/forgot-password/",
        {"email": "missing@example.com"},
        format="json",
    )

    assert response.status_code == 204
    assert len(mail.outbox) == 0


def test_auth_reset_password_updates_credentials_and_clears_require_reset(db) -> None:
    user = User.objects.create_user(
        email="reset@example.com",
        password="ChangeMe123!",
        require_password_reset=True,
    )
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    client = _csrf_client()

    response = client.post(
        f"{API_PREFIX}/auth/reset-password/",
        {
            "uid": uid,
            "token": token,
            "new_password": "NewPassword123!",
            "new_password_confirm": "NewPassword123!",
        },
        format="json",
    )

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.require_password_reset is False
    assert user.check_password("NewPassword123!")


def test_auth_change_password_requires_current_password_and_clears_require_reset(db) -> None:
    user = User.objects.create_user(
        email="change@example.com",
        password="ChangeMe123!",
        require_password_reset=True,
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    bad_response = client.post(
        f"{API_PREFIX}/auth/change-password/",
        {
            "current_password": "WrongPassword123!",
            "new_password": "UpdatedPassword123!",
            "new_password_confirm": "UpdatedPassword123!",
        },
        format="json",
    )
    assert bad_response.status_code == 400

    good_response = client.post(
        f"{API_PREFIX}/auth/change-password/",
        {
            "current_password": "ChangeMe123!",
            "new_password": "UpdatedPassword123!",
            "new_password_confirm": "UpdatedPassword123!",
        },
        format="json",
    )
    assert good_response.status_code == 204

    user.refresh_from_db()
    assert user.require_password_reset is False
    assert user.check_password("UpdatedPassword123!")


def test_auth_reauth_requires_authenticated_user(db) -> None:
    client = APIClient(enforce_csrf_checks=True)

    response = client.post(
        f"{API_PREFIX}/auth/re-auth/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )

    assert response.status_code == 401


def test_auth_reauth_sets_short_lived_reauth_cookie_on_success(db) -> None:
    user = User.objects.create_user(
        email="reauth@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    invalid_response = client.post(
        f"{API_PREFIX}/auth/re-auth/",
        {"current_password": "WrongPassword123!"},
        format="json",
    )
    assert invalid_response.status_code == 400

    success_response = client.post(
        f"{API_PREFIX}/auth/re-auth/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )

    assert success_response.status_code == 204
    assert settings.AUTH_REAUTH_COOKIE_NAME in client.cookies
    reauth_cookie = client.cookies[settings.AUTH_REAUTH_COOKIE_NAME].value
    assert has_recent_reauth_cookie(reauth_cookie, user) is True


def test_auth_session_reports_requires_mfa_step_up_for_system_admin_role(db) -> None:
    user = User.objects.create_user(
        email="system-admin-mfa@example.com",
        password="ChangeMe123!",
    )
    role = Group.objects.create(name="system_admin")
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=timezone.localdate(),
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")

    assert session_response.status_code == 200
    assert session_response.data["access"]["requires_mfa_step_up"] is True


def test_auth_session_reports_requires_mfa_step_up_for_opt_in_user(db) -> None:
    MfaPolicy.objects.update_or_create(
        policy_key="default",
        defaults={
            "enforce_for_all": False,
            "allow_user_opt_in": True,
        },
    )
    user = User.objects.create_user(
        email="opt-in-mfa@example.com",
        password="ChangeMe123!",
        mfa_enabled=True,
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")

    assert session_response.status_code == 200
    assert session_response.data["access"]["requires_mfa_step_up"] is True


def test_auth_session_does_not_require_mfa_when_opt_in_disabled_for_non_system_admin(db) -> None:
    MfaPolicy.objects.update_or_create(
        policy_key="default",
        defaults={
            "enforce_for_all": False,
            "allow_user_opt_in": False,
        },
    )
    user = User.objects.create_user(
        email="opt-in-disabled@example.com",
        password="ChangeMe123!",
        mfa_enabled=True,
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    session_response = client.get(f"{API_PREFIX}/auth/session/")
    assert session_response.status_code == 200
    assert session_response.data["access"]["requires_mfa_step_up"] is False


def test_auth_mfa_policy_can_be_updated_by_system_admin(db) -> None:
    user = User.objects.create_user(
        email="mfa-policy-admin@example.com",
        password="ChangeMe123!",
    )
    role = Group.objects.create(name="system_admin")
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=timezone.localdate(),
    )
    Group.objects.get_or_create(name="district_admin")
    Group.objects.get_or_create(name="teacher")
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    response = client.patch(
        f"{API_PREFIX}/auth/mfa/policy/",
        {
            "enforce_for_all": False,
            "allow_user_opt_in": True,
            "enforced_role_names": ["district_admin", "teacher"],
        },
        format="json",
    )
    assert response.status_code == 200
    assert response.data["enforce_for_all"] is False
    assert response.data["allow_user_opt_in"] is True
    assert response.data["enforced_role_names"] == ["district_admin", "teacher"]


def test_auth_mfa_policy_denies_non_system_admin_user(db) -> None:
    user = User.objects.create_user(
        email="mfa-policy-user@example.com",
        password="ChangeMe123!",
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    response = client.patch(
        f"{API_PREFIX}/auth/mfa/policy/",
        {"enforce_for_all": True},
        format="json",
    )
    assert response.status_code == 403


def test_auth_mfa_challenge_and_verify_enable_privileged_step_up_hook(db) -> None:
    mail.outbox.clear()
    user = User.objects.create_user(
        email="mfa-hook@example.com",
        password="ChangeMe123!",
    )
    role = Group.objects.create(name="system_admin")
    role.permissions.add(
        Permission.objects.get(content_type__app_label="auth", codename="view_group")
    )
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=timezone.localdate(),
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    pre_hook_response = client.get(f"{API_PREFIX}/auth/privileged-review-hook/")
    assert pre_hook_response.status_code == 403

    reauth_response = client.post(
        f"{API_PREFIX}/auth/re-auth/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )
    assert reauth_response.status_code == 204

    without_mfa_response = client.get(f"{API_PREFIX}/auth/privileged-review-hook/")
    assert without_mfa_response.status_code == 403

    challenge_response = client.post(
        f"{API_PREFIX}/auth/mfa/challenge/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )
    assert challenge_response.status_code == 200
    assert "challenge_id" in challenge_response.data
    assert len(mail.outbox) == 1
    challenge_id = challenge_response.data["challenge_id"]
    code = mail.outbox[0].body.strip().split()[-1]

    verify_response = client.post(
        f"{API_PREFIX}/auth/mfa/verify/",
        {"challenge_id": challenge_id, "code": code},
        format="json",
    )
    assert verify_response.status_code == 204
    assert settings.AUTH_MFA_COOKIE_NAME in client.cookies

    post_hook_response = client.get(f"{API_PREFIX}/auth/privileged-review-hook/")
    assert post_hook_response.status_code == 200


def test_auth_session_review_and_revoke_all_sessions_require_step_up_and_revoke_tokens(db) -> None:
    mail.outbox.clear()
    user = User.objects.create_user(
        email="session-review@example.com",
        password="ChangeMe123!",
    )
    role = Group.objects.create(name="system_admin")
    role.permissions.add(
        Permission.objects.get(content_type__app_label="auth", codename="view_group")
    )
    RoleAssignment.objects.create(
        user=user,
        role=role,
        starts_on=timezone.localdate(),
    )
    client = _csrf_client()
    client.post(
        f"{API_PREFIX}/auth/login/",
        {"email": user.email, "password": "ChangeMe123!"},
        format="json",
    )

    pre_review_response = client.get(f"{API_PREFIX}/auth/session-review/")
    assert pre_review_response.status_code == 403

    client.post(
        f"{API_PREFIX}/auth/re-auth/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )
    challenge_response = client.post(
        f"{API_PREFIX}/auth/mfa/challenge/",
        {"current_password": "ChangeMe123!"},
        format="json",
    )
    challenge_id = challenge_response.data["challenge_id"]
    code = mail.outbox[0].body.strip().split()[-1]
    client.post(
        f"{API_PREFIX}/auth/mfa/verify/",
        {"challenge_id": challenge_id, "code": code},
        format="json",
    )

    review_response = client.get(f"{API_PREFIX}/auth/session-review/")
    assert review_response.status_code == 200
    assert review_response.data["auth_session_version"] == 1
    assert review_response.data["mfa_required_for_user"] is True

    old_refresh = client.cookies["ik12_refresh"].value
    revoke_response = client.post(f"{API_PREFIX}/auth/sessions/revoke-all/", {}, format="json")
    assert revoke_response.status_code == 204
    assert revoke_response.cookies["ik12_access"].value == ""
    assert revoke_response.cookies["ik12_refresh"].value == ""

    client.cookies["ik12_refresh"] = old_refresh
    refresh_response = client.post(f"{API_PREFIX}/auth/refresh/", {}, format="json")
    assert refresh_response.status_code == 401
    assert refresh_response.data["detail"] == "Session has been revoked."
