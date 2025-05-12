from customers.repositories.respository import CustomerRepository


class CustomerRepositoryFactory:
    def get_repository(self):
        return CustomerRepository()

