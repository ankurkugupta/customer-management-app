from django.urls import path


from customers.interface.apis import CustomerCreateApi, CustomerDeleteApi, CustomerUpdateApi, CustomerFetchAllApi

urlpatterns=[
   ##### REST API ########
   path("add/",CustomerCreateApi.as_view(),name="customer_add_api"),
   path("<int:customer_id>/delete/", CustomerDeleteApi.as_view(), name="customer_delete_api"),
   path("<int:customer_id>/update/",CustomerUpdateApi.as_view(),name="customer_update_api"),
   path("fetch-all/",CustomerFetchAllApi.as_view(),name="customer_fetch_all_api"),


]