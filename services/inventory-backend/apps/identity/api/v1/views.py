from rest_framework import status  # type: ignore[import-untyped]
from rest_framework.permissions import IsAuthenticated  # type: ignore[import-untyped]
from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.response import Response  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]
from rest_framework_simplejwt.tokens import RefreshToken  # type: ignore[import-untyped]

from .permissions import HasElevatedRole
from .serializers import LoginSerializer, LogoutSerializer, RefreshSerializer, UserSummarySerializer


class LoginView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes: list[type] = []

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshView(APIView):  # type: ignore[misc]
    authentication_classes: list[type] = []
    permission_classes: list[type] = []

    def post(self, request: Request) -> Response:
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = RefreshToken(serializer.validated_data["refresh"])
        refresh.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(UserSummarySerializer(request.user).data, status=status.HTTP_200_OK)


class RbacCheckView(APIView):  # type: ignore[misc]
    permission_classes = [IsAuthenticated, HasElevatedRole]

    def get(self, request: Request) -> Response:
        return Response({"status": "allowed"}, status=status.HTTP_200_OK)
