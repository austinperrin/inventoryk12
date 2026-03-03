from django.contrib.auth import authenticate, get_user_model
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
