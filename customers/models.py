from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from customers.repositories.querysets import CustomerQuerySet
from users.models import User


# Create your models here.

class CreateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='created_%(class)s_objects')

    class Meta:
        abstract = True

class UpdateModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='updated_%(class)s_objects',null=True,blank=True)

    class Meta:
        abstract = True

class DeleteModel(models.Model):
    deleted_at = models.DateTimeField(blank=True,null=True)
    deleted_by = models.ForeignKey(User,on_delete=models.RESTRICT,related_name='deleted_%(class)s_objects',null=True,blank=True)

    def soft_delete(self,deleted_by_id:int):
        self.deleted_at=timezone.now()
        self.deleted_by_id=deleted_by_id
        self.save()

    class Meta:
        abstract = True


class CreateUpdateDeleteAbstractModel(CreateModel,UpdateModel,DeleteModel):
    class Meta:
        abstract = True


class Customer(CreateUpdateDeleteAbstractModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()

    objects = CustomerQuerySet.as_manager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def customer_age(self):
        return timezone.now().year-self.date_of_birth.year


    class Meta:
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(fields=['phone_number'],
                                    name='unique_phone_number',
                                    condition=models.Q(deleted_at=None)),
        ]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        db_table = "customers"

