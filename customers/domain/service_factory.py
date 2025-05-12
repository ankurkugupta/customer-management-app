from customers.domain.services import CustomerService


class CustomerServiceFactory:
    def get_customer_service(self, repository):
        return CustomerService(repository=repository)