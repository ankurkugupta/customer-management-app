from django.urls import path

from customers.interface.views import AddCustomerView, ModifyCustomerView, DeleteCustomerView, DashboardView

urlpatterns=[
path('dashboard/', DashboardView.as_view(), name='dashboard'),
path("create/", AddCustomerView.as_view(), name="add_customer_view"),
path('<int:pk>/modify/', ModifyCustomerView.as_view(), name='modify_customer_view'),
path('<int:pk>/delete/', DeleteCustomerView.as_view(), name='delete_customer_view'),
]