from django.db.models import Q
from django.core.exceptions import ValidationError

from users.models import User


class UserService:
    def _check_if_user_exists(self, email, phone_number):

        return User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists()

    def create_user(self,
                    first_name:str,
                    last_name:str,
                    email:str,
                    password:str,
                    phone_number:str
                    ):

        if self._check_if_user_exists(email=email, phone_number=phone_number):
            raise ValidationError("User already exists")

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=email,
                    phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

