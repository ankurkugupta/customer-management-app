from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from customers.models import Customer


class CustomerCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = PhoneNumberField(region="IN")
    date_of_birth = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        ref_name = "CustomerInputSerializer"


class CustomerModelSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()

    def get_age(self,obj):
        return obj.customer_age

    class Meta:
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'date_of_birth',"age"]
        model = Customer
        ref_name = "CustomerModelSerializer"



class CustomerFilterSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()

    class Meta:
        ref_name = "FilterSerializer"

class CustomerUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField(required=False)
    date_of_birth = serializers.DateField(format="%Y-%m-%d",required=False)

    def validate(self, attrs):
        if not any(attrs.values()):
            raise serializers.ValidationError("At least one field should be provided")
        return attrs

    class Meta:
        ref_name = "CustomerUpdateSerializer"

