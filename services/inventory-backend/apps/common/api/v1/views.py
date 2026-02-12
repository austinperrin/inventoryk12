from rest_framework.request import Request  # type: ignore[import-untyped]
from rest_framework.response import Response  # type: ignore[import-untyped]
from rest_framework.views import APIView  # type: ignore[import-untyped]


class HealthCheckView(APIView):  # type: ignore[misc]
    """
    Lightweight health check endpoint for service monitoring and uptime probes.
    """

    authentication_classes: list[type] = []
    permission_classes: list[type] = []

    def get(self, request: Request) -> Response:
        return Response({"status": "ok"})
