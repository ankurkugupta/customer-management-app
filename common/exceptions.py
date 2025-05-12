from django.core.exceptions import ValidationError


class CustomValidationError(ValidationError):
    pass
