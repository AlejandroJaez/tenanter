from django.contrib.auth.models import User
from django.db import models
from easy_tenants import get_current_tenant
from easy_tenants.models import TenantManager, TenantAwareAbstract


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Domain(models.Model):
    tenant = models.ForeignKey(Customer, on_delete=models.CASCADE)
    domain = models.CharField(max_length=253, unique=True, db_index=True)

    def __str__(self):
        return str(self.domain)


class Product(models.Model):
    tenant = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    objects = TenantManager()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Set tenant field on save"""
        tenant_id = self.tenant_id
        setattr(self, "tenant", get_current_tenant())
        self.tenant_id = tenant_id
        super().save(*args, **kwargs)
