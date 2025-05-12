from django_extensions.management.commands.export_emails import full_name
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from common.validators import validate_name
from customers.models import Customer




class CustomerCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50,required=False,allow_null=True,allow_blank=True)
    phone_number = PhoneNumberField(region="IN")
    date_of_birth = serializers.DateField(format="%Y-%m-%d")

    def validate(self, attrs):
        errors=[]
        if not validate_name(attrs.get("first_name")):
            errors.append({"first_name":"Only Character Allowed"})
        if  attrs.get("last_name") and not validate_name(attrs.get("first_name")):
            errors.append({"last_name":"Only Character Allowed"})

        if errors:
            raise serializers.ValidationError(errors)
        return attrs


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
    first_name = serializers.CharField(required=False,max_length=50)
    last_name = serializers.CharField(required=False,max_length=50,allow_null=True,allow_blank=True)
    phone_number = PhoneNumberField(required=False)
    date_of_birth = serializers.DateField(format="%Y-%m-%d",required=False)

    def validate(self, attrs):
        if not any(attrs.values()):
            raise serializers.ValidationError("At least one field should be provided")

        errors=[]
        if attrs.get("first_name") and not validate_name(attrs.get("first_name")):
            errors.append({"first_name":"Only Character Allowed"})
        if  attrs.get("last_name") and not validate_name(attrs.get("first_name")):
            errors.append({"last_name":"Only Character Allowed"})

        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    class Meta:
        ref_name = "CustomerUpdateSerializer"

