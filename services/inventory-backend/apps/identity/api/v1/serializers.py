from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "uuid", "email", "first_name", "last_name", "full_name")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        authenticated_user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if authenticated_user is None or not authenticated_user.is_active:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = authenticated_user
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        return value.strip().lower()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(trim_whitespace=False, write_only=True)
    new_password_confirm = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        new_password = attrs["new_password"]
        confirm_password = attrs["new_password_confirm"]
        if new_password != confirm_password:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})

        user = self._resolve_user(attrs["uid"])
        if user is None:
            raise serializers.ValidationError({"uid": "Invalid reset token."})
        if not default_token_generator.check_token(user, attrs["token"]):
            raise serializers.ValidationError({"token": "Invalid reset token."})

        try:
            validate_password(new_password, user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"new_password": list(exc.messages)}) from exc

        attrs["user"] = user
        return attrs

    def _resolve_user(self, uid: str):
        try:
            decoded_uid = force_str(urlsafe_base64_decode(uid))
            return User.objects.get(pk=decoded_uid, is_active=True)
        except Exception:
            return None


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(trim_whitespace=False, write_only=True)
    new_password = serializers.CharField(trim_whitespace=False, write_only=True)
    new_password_confirm = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})

        try:
            validate_password(attrs["new_password"], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"new_password": list(exc.messages)}) from exc

        return attrs


class ReauthSerializer(serializers.Serializer):
    current_password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        return attrs
