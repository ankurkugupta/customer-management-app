import abc
import datetime

from django.db.models import QuerySet

from customers.models import Customer


class AbstractCustomerRepository:
    @abc.abstractmethod

    def add_customer(self, first_name:str, last_name:str, phone_number:str, date_of_birth:datetime.date, created_by_id:int)->Customer:
        pass

    def get_customer(self, customer_id:int)->Customer:
        pass

    def update_customer(self, customer_id:int,updated_by_id:int, first_name:str=None, last_name:str=None, phone_number:str=None, date_of_birth:datetime.date=None):
        pass

    def delete_customer(self, customer_id:int,deleted_by_id:int):
        pass

    def get_all_customers(self)->QuerySet[Customer]:
        pass


