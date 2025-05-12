from django import forms
from users.models import User
from phonenumber_field.formfields import PhoneNumberField

class UserRegistrationForm(forms.ModelForm):
    phone_number = PhoneNumberField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password','phone_number']

