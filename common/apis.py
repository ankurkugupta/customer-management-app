from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class BaseApi(APIView):
    permission_classes = [IsAuthenticated]
    input_serializer=None
    custom_message=None

    def validate_input_data(self,data):
        if not self.input_serializer or isinstance(self.input_serializer,serializers.Serializer):
            raise serializers.ValidationError("input_serializer is not defined or invalid")
        if not data or not isinstance(data,dict):
            raise serializers.ValidationError("Invalid input data")

        serializer = self.input_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
