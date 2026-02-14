from rest_framework.permissions import BasePermission  # type: ignore[import-untyped]
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]

ELEVATED_ROLES = {
    "district_admin",
    "site_admin",
    "system_admin",
    "principal",
}


class HasElevatedRole(BasePermission):  # type: ignore[misc]
    """
    Grants access only to users in elevated, staff-side roles.
    """

    message = "User does not have a required elevated role."

    def has_permission(self, request: Request, view: APIView) -> bool:
        user = request.user
        if not user or not user.is_authenticated:
            return False

        user_roles = set(user.groups.values_list("name", flat=True))
        return bool(user_roles & ELEVATED_ROLES)
