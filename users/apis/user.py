# views.py
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from common.apis import BaseApi
from users.serializers import LogoutInputSerializer, UserRegistrationSerializer, UserModelSerializer
from users.services import UserService


class LogoutAPI(BaseApi):
    input_serializer = LogoutInputSerializer

    @swagger_auto_schema(
    operation_id="logout_api",
    operation_summary="Logout a user",
    request_body=LogoutInputSerializer(),
    responses={status.HTTP_200_OK: "Successfully logged out"},
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            self.custom_message="Refresh token is required"
            return Response( status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            self.custom_message="Successfully logged out"
            return Response(status=status.HTTP_200_OK)
        except TokenError:
            self.custom_message="Invalid refresh token"
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationAPI(BaseApi):
    permission_classes = [AllowAny]
    input_serializer = UserRegistrationSerializer

    @swagger_auto_schema(
    operation_id="user_registration_api",
    operation_summary="User Registration API",
    request_body=UserRegistrationSerializer(),
    responses={status.HTTP_200_OK: UserModelSerializer()},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        validated_data = self.validate_input_data(request.data)
        user=UserService().create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
            phone_number=validated_data.get('phone_number'),
        )
        self.custom_message="User created successfully"

        return Response(data=UserModelSerializer(user).data,
            status=status.HTTP_200_OK)


