from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.response import Response

from common.apis import BaseApi
from customers.repositories.repo_factories import CustomerRepositoryFactory
from customers.interface.serializers import CustomerCreateSerializer, CustomerModelSerializer, CustomerUpdateSerializer
from customers.domain.service_factory import CustomerServiceFactory


class CustomerCreateApi(BaseApi):
    input_serializer = CustomerCreateSerializer

    @swagger_auto_schema(
        request_body=CustomerCreateSerializer,
        responses={201: CustomerCreateSerializer()},
        operation_id="customer_create_api",
        operation_summary="Create a new customer object via this API",
    )
    @transaction.atomic
    def post(self, request,*args,**kwargs):
        data = self.validate_input_data(request.data)
        customer_service_obj=CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository(
            )
        )
        customer=customer_service_obj.add_customer(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            date_of_birth=data.get('date_of_birth'),
            created_by_id=request.user.id
        )
        self.custom_message="Customer created successfully"
        return Response(
            CustomerModelSerializer(customer).data,
            status=status.HTTP_201_CREATED
        )

class CustomerDeleteApi(BaseApi):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: "Customer deleted successfully"},
        operation_id="customer_delete_api",
        operation_summary="Delete customer object via this API",
    )
    @transaction.atomic
    def delete(self, request,customer_id,*args,**kwargs):
        customer_service_obj=CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository(
            )
        )
        customer_service_obj.delete_customer(
            customer_id=customer_id,deleted_by_id=request.user.id
        )
        self.custom_message="Customer deleted successfully"
        return Response(status=status.HTTP_200_OK)

class CustomerUpdateApi(BaseApi):
    input_serializer = CustomerUpdateSerializer

    @swagger_auto_schema(
        request_body=CustomerCreateSerializer,
        responses={201: CustomerCreateSerializer()},
        operation_id="customer_update_api",
        operation_summary="Update a customer object via this API",
    )
    @transaction.atomic
    def put(self, request,customer_id,*args,**kwargs):
        data = self.validate_input_data(request.data)
        customer_service_obj=CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository(
            )
        )
        customer=customer_service_obj.update_customer(
            customer_id=customer_id,
            updated_by_id=request.user.id,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone_number=data.get('phone_number'),
            date_of_birth=data.get('date_of_birth'),
        )

        self.custom_message="Customer created successfully"
        return Response(
            data=CustomerModelSerializer(customer).data,
            status=status.HTTP_201_CREATED

        )

class CustomerFetchAllApi(BaseApi):

    @swagger_auto_schema(
        responses={201: CustomerModelSerializer(many=True)},
        operation_id="customer_fetch_all_api",
        operation_summary="Get all customers object via this API",
    )

    def get_queryset(self):
        customer_service_obj=CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository()
        )
        customers=customer_service_obj.get_all_customers()
        return customers

    def get(self, request,*args,**kwargs):
        customers = self.get_queryset()
        self.custom_message="Customers Fetch Successfully" if customers else "No Customers Found"
        paginator = LimitOffsetPagination()

        paginated_customers = paginator.paginate_queryset(customers, request)
        serializer = CustomerModelSerializer(paginated_customers, many=True)

        return paginator.get_paginated_response(serializer.data)



