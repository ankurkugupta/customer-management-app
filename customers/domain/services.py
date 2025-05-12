import datetime

from customers.domain.interfaces.customer_repository import AbstractCustomerRepository


class CustomerService:
    def __init__(self, repository: AbstractCustomerRepository):
        self.repository = repository

    def get_all_customers(self):
        return self.repository.get_all_customers()

    def add_customer(self, first_name:str, last_name:str, phone_number:str, date_of_birth:datetime.date, created_by_id:int):
        return self.repository.add_customer(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                created_by_id=created_by_id
        )

    def update_customer(self, customer_id:int,updated_by_id:int, first_name=None, last_name=None, phone_number=None, date_of_birth=None,):
        return self.repository.update_customer(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                updated_by_id=updated_by_id
        )

    def delete_customer(self, customer_id:int,deleted_by_id:int):
        return self.repository.delete_customer(customer_id=customer_id,deleted_by_id=deleted_by_id)