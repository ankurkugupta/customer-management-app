from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from users.models import User


class LogoutInputSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        ref_name = "LogoutInputSerializer"


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    phone_number = PhoneNumberField()

    class Meta:
        ref_name = "UserRegistrationSerializer"


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']
        model = User
        ref_name = "UserModelSerializer"