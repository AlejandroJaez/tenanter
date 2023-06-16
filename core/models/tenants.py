from django.contrib.auth.models import User
from django.db import models
from easy_tenants import get_current_tenant
from easy_tenants.models import TenantManager, TenantAwareAbstract

from config import settings

field_name = settings.EASY_TENANTS_TENANT_FIELD


# Create your models here.
class Tenant(models.Model):
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Domain(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    domain = models.CharField(max_length=253, unique=True, db_index=True)

    def __str__(self):
        return str(self.domain)