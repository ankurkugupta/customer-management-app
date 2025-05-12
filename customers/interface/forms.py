
from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField

from django.core.exceptions import ValidationError

from common.validators import validate_name


class CustomCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name',required=False)
    phone_number = PhoneNumberField(label='Phone Number')
    date_of_birth = forms.DateField(
        label='Date of Birth',
        initial=None,
        widget = SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=range(timezone.now().year - 100, timezone.now().year-15)),
        )

    def clean_first_name(self):
        first_name=self.cleaned_data['first_name']
        if not validate_name(first_name):
                raise ValidationError("First Name must contain only letters.")
        return first_name


    def clean_last_name(self):
        first_name=self.cleaned_data['last_name']
        if first_name and not validate_name(first_name):
                raise ValidationError("Last Name must contain only letters.")
        return first_name


