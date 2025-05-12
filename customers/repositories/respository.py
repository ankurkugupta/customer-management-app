from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

from customers.domain.interfaces.customer_repository import AbstractCustomerRepository
from customers.models import Customer


class CustomerRepository(AbstractCustomerRepository):

    def add_customer(self, first_name, last_name, phone_number, date_of_birth, created_by_id):
        try:
            customer = Customer(first_name=first_name, last_name=last_name, phone_number=phone_number,
                                date_of_birth=date_of_birth,created_by_id=created_by_id)
            customer.full_clean()
            customer.save()
            return customer
        except ValidationError as e:
            raise ValidationError({"Invalid data":str(e)}) from e

        except IntegrityError as e:
            raise ValidationError("Unable to save data") from e

    def get_customer(self, customer_id):
        try:
            customer = Customer.objects.available().get(id=customer_id)
            return customer
        except ObjectDoesNotExist as e:
            raise ValidationError("Customer ID does not exist")

    def update_customer(self, customer_id:int,updated_by_id:int, first_name=None, last_name=None, phone_number=None, date_of_birth=None):
        try:
            customer = Customer.objects.available().get(id=customer_id)
            if first_name:
                customer.first_name = first_name
            if last_name:
                customer.last_name = last_name
            if phone_number:
                customer.phone_number = phone_number
            if date_of_birth:
                customer.date_of_birth = date_of_birth

            customer.updated_by_id = updated_by_id
            customer.full_clean()
            customer.save()
            return customer
        except ObjectDoesNotExist as e:
            raise ValidationError("Customer ID does not exist")

    def delete_customer(self, customer_id:int,deleted_by_id:int):
        try:
            customer = Customer.objects.available().get(id=customer_id)
            customer.soft_delete(deleted_by_id=deleted_by_id)
            return
        except ObjectDoesNotExist as e:
            raise ValidationError("Customer ID does not exist")

    def get_all_customers(self):
        return Customer.objects.all().available()


