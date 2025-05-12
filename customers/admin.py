from django.contrib import admin
from django.utils import timezone

from customers.models import Customer


# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id",'full_name', 'phone_number', 'date_of_birth','age')
    ordering = ('-id',)

    def age(self, obj):
        return timezone.now().date().year-obj.date_of_birth.year

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    full_name.short_description = "Full Name"
    age.short_description = "Age"
    age.description = "Age Of Customer"

admin.site.register(Customer, CustomerAdmin)