from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from customers.domain.interfaces.customer_repository import AbstractCustomerRepository
from customers.models import Customer


import logging

logger = logging.getLogger(__name__)

class ExceptionConstants:
    PHONE_NUMBER_ALREADY_EXISTS = "Phone number already exists"
    CUSTOMER_DOES_NOT_EXISTS = "Customer does not exist"

class CustomerRepository(AbstractCustomerRepository):
    """
    Concrete implementation of the AbstractCustomerRepository for managing Customer records.

    This class handles all database operations related to the Customer model, including
    creation, retrieval, updating, deletion, and listing of customers.

    It enforces business rules such as ensuring phone number uniqueness and validating
    the existence of customer records before performing operations.
    """

    def add_customer(self, first_name, last_name, phone_number, date_of_birth, created_by_id):
        try:
            customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone_number,
                                date_of_birth=date_of_birth,created_by_id=created_by_id)
            customer.full_clean()
            customer.save()
            return customer
        except ValidationError as e:
            if "phone_number_unique" in str(e):
                raise self.DuplicatePhoneNumber(ExceptionConstants.PHONE_NUMBER_ALREADY_EXISTS) from e
            raise ValidationError(f"Invalid data,{str(e)}") from e

        except IntegrityError as e:
            raise self.DuplicatePhoneNumber(ExceptionConstants.PHONE_NUMBER_ALREADY_EXISTS) from e

    def get_customer(self, customer_id):
        try:
            customer = Customer.objects.available().get(id=customer_id)
            return customer
        except ObjectDoesNotExist as e:
            logger.info(f"{ExceptionConstants.CUSTOMER_DOES_NOT_EXISTS}",customer_id)
            raise self.CustomerDoesNotExist(ExceptionConstants.CUSTOMER_DOES_NOT_EXISTS)

    def update_customer(self, customer_id:int,updated_by_id:int, first_name=None, last_name=None, phone_number=None, date_of_birth=None):
        try:
            customer = Customer.objects.available().get(id=customer_id)

            updated_fields = []
            field_map = {
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
                "date_of_birth": date_of_birth,
            }

            for field, new_value in field_map.items():
                if new_value or ""==new_value and getattr(customer, field) != new_value:
                    setattr(customer, field, new_value)
                    updated_fields.append(field)

            if updated_fields:
                customer.updated_by_id = updated_by_id
                customer.full_clean()
                customer.save()
                logger.info(f"customer {customer.id} field updated by {updated_by_id}",updated_fields)
            return customer
        except ValidationError as e:
            if "phone_number_unique" in str(e):
                raise self.DuplicatePhoneNumber(ExceptionConstants.PHONE_NUMBER_ALREADY_EXISTS) from e
            raise ValidationError(f"Invalid data,{str(e)}") from e
        except ObjectDoesNotExist as e:
            raise self.CustomerDoesNotExist(ExceptionConstants.CUSTOMER_DOES_NOT_EXISTS)
        except IntegrityError as e:
            raise self.DuplicatePhoneNumber(ExceptionConstants.PHONE_NUMBER_ALREADY_EXISTS)


    def delete_customer(self, customer_id:int,deleted_by_id:int):
        try:
            customer = Customer.objects.available().get(id=customer_id)
            customer.soft_delete(deleted_by_id=deleted_by_id)
            return
        except ObjectDoesNotExist as e:
            raise self.CustomerDoesNotExist(ExceptionConstants.CUSTOMER_DOES_NOT_EXISTS)

    def get_all_customers(self):
        return Customer.objects.all().available()


