import datetime

from django.utils import timezone

from common.exceptions import CustomValidationError
from common.validators import validate_user_age
from customers.domain.interfaces.customer_repository import AbstractCustomerRepository

class MessageConstants:
    CUSTOMER_DOES_NOT_EXISTS = "Customer does not exists"
    CUSTOMER_AGE_NOT_VALID = "Customer Age not valid"
    CUSTOMER_ALREADY_EXISTS="Customer with this phone number already exists."

class CustomerService:
    """
    Service layer for managing customer-related business logic.

    This class acts as an intermediary between views/apis and the customer repository.
    It handles validation, exception translation, and delegates data access to the repository.

    Responsibilities:
        - Validate customer age before creation.
        - Catch and re-raise repository exceptions as service-level exceptions with user-friendly messages.
        - Provide high-level operations for creating, updating, deleting, and retrieving customers.

    Exceptions:
        CustomerServiceException: Raised when business rules are violated or repository errors occur.
    """
    class CustomerServiceException(CustomValidationError):
        pass

    def __init__(self, repository: AbstractCustomerRepository):
        self.repository = repository

    def get_all_customers(self):
        return self.repository.get_all_customers()

    def check_if_customer_age_valid(self,date_of_birth):
        return validate_user_age(date_of_birth=date_of_birth)

    def add_customer(self, first_name:str, last_name:str, phone_number:str, date_of_birth:datetime.date, created_by_id:int):
        if not self.check_if_customer_age_valid(date_of_birth=date_of_birth):
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_AGE_NOT_VALID)
        try:
            customer=self.repository.add_customer(
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    created_by_id=created_by_id
            )
            return customer
        except self.repository.CustomerDoesNotExist:
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_DOES_NOT_EXISTS)
        except self.repository.DuplicatePhoneNumber:
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_ALREADY_EXISTS)

    def update_customer(self, customer_id:int,updated_by_id:int, first_name=None, last_name=None, phone_number=None, date_of_birth=None,):
        try:
            customer= self.repository.update_customer(
                    customer_id=customer_id,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    updated_by_id=updated_by_id
            )
            return customer
        except self.repository.CustomerDoesNotExist:
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_DOES_NOT_EXISTS)
        except self.repository.DuplicatePhoneNumber:
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_ALREADY_EXISTS)

    def delete_customer(self, customer_id:int,deleted_by_id:int):
        try:
            self.repository.delete_customer(customer_id=customer_id,deleted_by_id=deleted_by_id)
        except self.repository.CustomerDoesNotExist:
            raise self.CustomerServiceException(MessageConstants.CUSTOMER_DOES_NOT_EXISTS)