from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ProtectedApi(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="protected_view_health_checkApi",
        operation_summary="Check if you are authenticated",
        tags=["Health Check"]
    )
    def get(self, request):
        return Response({"message": "You are authenticated"},status.HTTP_200_OK)



class AllowAllHealthCheckApi(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Check if you are Allowed directly",
        operation_id="allow_all_health_check",
        tags=["Health Check"]
    )
    def get(self, request):
        return Response({"message": "You are Allowed directly"},status=status.HTTP_200_OK)