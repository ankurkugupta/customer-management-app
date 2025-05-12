import abc
import datetime

from django.db.models import QuerySet

from common.exceptions import CustomValidationError
from customers.models import Customer


class AbstractCustomerRepository:
    """
    Abstract base class that defines the contract for customer-related operations.

    This class should be inherited by concrete repository implementations that
    handle data access logic for the Customer model. All core CRUD methods must be
    implemented by subclasses.

    Exceptions:
        DuplicatePhoneNumber: Raised when a phone number already exists in the system.
        CustomerDoesNotExist: Raised when the requested customer does not exist.

    """
    class DuplicatePhoneNumber(CustomValidationError):
        pass
    class CustomerDoesNotExist(CustomValidationError):
        pass

    @abc.abstractmethod
    def add_customer(self, first_name:str, last_name:str, phone_number:str, date_of_birth:datetime.date, created_by_id:int)->Customer:
        pass

    @abc.abstractmethod
    def get_customer(self, customer_id:int)->Customer:
        pass

    @abc.abstractmethod
    def update_customer(self, customer_id:int,updated_by_id:int, first_name:str=None, last_name:str=None, phone_number:str=None, date_of_birth:datetime.date=None):
        pass

    @abc.abstractmethod
    def delete_customer(self, customer_id:int,deleted_by_id:int):
        pass

    @abc.abstractmethod
    def get_all_customers(self)->QuerySet[Customer]:
        pass


