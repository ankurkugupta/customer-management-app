from email.policy import default

from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField

from django.contrib.admin.widgets import AdminDateWidget
class CustomCustomerForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    phone_number = PhoneNumberField(label='Phone Number')
    date_of_birth = forms.DateField(
        label='Date of Birth',
        initial=None,
        widget = SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=range(timezone.now().year - 100, timezone.now().year-15)),
        )





