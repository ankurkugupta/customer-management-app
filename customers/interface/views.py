from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from common.exceptions import CustomValidationError
from customers.interface.forms import CustomCustomerForm
from customers.models import Customer
from customers.repositories.repo_factories import CustomerRepositoryFactory
from customers.domain.service_factory import CustomerServiceFactory

import logging

logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, View):
    template_name = 'customers/dashboard.html'
    login_url = 'login'

    def get_customers(self):
        customer_service_obj=CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository()
        )
        customers=customer_service_obj.get_all_customers()

        return customers

    def get_context_data(self, **kwargs):
        context = dict()
        context['customers'] = self.get_customers()

        messages.success(self.request, 'Customers fetched successfully.')
        return context

    def get(self, request):
        customers=self.get_customers()
        paginator = Paginator(customers, 10)  # Show 10 customers per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'customers': page_obj,  # this will be used in the template
        }
        logger.info(f"User accessed the dashboard,{request.user.id},{request.user.username}")
        messages.success(self.request, 'Customers fetched successfully.')
        return render(request, self.template_name, context)



class AddCustomerView(LoginRequiredMixin, View):
    template_name = 'customers/add_customer.html'

    def get(self, request):
        form = CustomCustomerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomCustomerForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        customer_service_obj = CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository(
            )
        )
        try:
            customer_service_obj.add_customer(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            phone_number=form.cleaned_data['phone_number'],
            date_of_birth=form.cleaned_data['date_of_birth'],
            created_by_id=self.request.user.id
        )
        except CustomValidationError as e:
            messages.error(request, " ".join(e.messages))
            return render(request, self.template_name, {'form': form})
        messages.success(request, 'Customer added successfully.')
        return redirect('dashboard')




class DeleteCustomerView(LoginRequiredMixin, View):
    template_name = 'customers/confirm_delete.html'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        return render(request, self.template_name, {'customer': customer})

    def post(self, request, pk):
        try:
            customer_service_obj = CustomerServiceFactory().get_customer_service(
                repository=CustomerRepositoryFactory().get_repository(
                )
            )
            customer_service_obj.delete_customer(
                customer_id=pk, deleted_by_id=self.request.user.id
            )
        except CustomValidationError as e:
            messages.error(request,"".join(e.messages))

        messages.success(request, 'Customer deleted successfully.')
        return redirect('dashboard')



class ModifyCustomerView(View):
    template_name = 'customers/modify_customer.html'

    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomCustomerForm(initial={
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'phone_number': customer.phone_number,
            'date_of_birth': customer.date_of_birth
        })
        return render(request, self.template_name, {'form': form, 'customer': customer})

    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        form = CustomCustomerForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form, 'customer': customer})
        customer_service_obj = CustomerServiceFactory().get_customer_service(
            repository=CustomerRepositoryFactory().get_repository(
            )
        )
        try:
            customer_service_obj.update_customer(
                updated_by_id=self.request.user.id,
                customer_id=customer.id,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                date_of_birth=form.cleaned_data['date_of_birth'],
            )
        except CustomValidationError as e:
            messages.error(request, " ".join(e.messages))
            return render(request, self.template_name, {'form': form, 'customer': customer})

        messages.success(request, 'Customer updated successfully.')
        return redirect('dashboard')
