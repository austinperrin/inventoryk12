from typing import Any

from rest_framework.exceptions import AuthenticationFailed  # type: ignore[import-untyped]
from rest_framework import serializers  # type: ignore[import-untyped]
from rest_framework_simplejwt.serializers import (  # type: ignore[import-untyped]
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class UserSummarySerializer(serializers.Serializer):  # type: ignore[misc]
    id = serializers.IntegerField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    roles = serializers.ListField(child=serializers.CharField(), read_only=True)

    def to_representation(self, instance: Any) -> dict[str, object]:
        data = super().to_representation(instance)
        if hasattr(instance, "active_role_names"):
            data["roles"] = instance.active_role_names()
        else:
            data["roles"] = sorted(instance.groups.values_list("name", flat=True))
        return data


class LoginSerializer(TokenObtainPairSerializer):  # type: ignore[misc]
    """
    Email/password login serializer that returns JWT pair + user summary.
    """

    def validate(self, attrs: dict[str, object]) -> dict[str, str]:
        data = super().validate(attrs)
        if not self.user.is_superuser and not self.user.has_active_role_assignment():
            raise AuthenticationFailed("User does not have an active role assignment.")
        data["user"] = UserSummarySerializer(self.user).data  # type: ignore[assignment]
        return data  # type: ignore[return-value]


class RefreshSerializer(TokenRefreshSerializer):  # type: ignore[misc]
    """JWT refresh serializer wrapper for consistent local API imports."""


class LogoutSerializer(serializers.Serializer):  # type: ignore[misc]
    refresh = serializers.CharField(required=True)
