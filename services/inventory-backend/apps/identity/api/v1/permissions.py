from rest_framework.permissions import BasePermission
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]

from apps.identity.services import resolve_user_access


class HasEffectiveAccess(BasePermission):
    message = "No effective access is available for this account."

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        access = resolve_user_access(request.user)
        self.message = str(access.get("no_access_message") or self.message)
        return bool(access["has_effective_access"])
