import re
from datetime import date

from django.utils import timezone


def validate_user_age(date_of_birth:date):
    if 15 <= (timezone.now().date().year - date_of_birth.year) <= 100:
        return True
    return False


def validate_name(name):
    pattern = r"^[A-Za-z]+( [A-Za-z]+)*$"
    return bool(re.fullmatch(pattern, name))
