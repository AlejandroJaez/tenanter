from django.db import models
from easy_tenants import get_current_tenant
from easy_tenants.models import TenantManager

from config import settings
from core.models import Tenant

field_name = settings.EASY_TENANTS_TENANT_FIELD


class Product(models.Model):
    tenant = models.ForeignKey(to=Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    objects = TenantManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Set tenant field on save"""
        if getattr(self, "tenant_id") is None:
            setattr(self, field_name, get_current_tenant())

        super().save(*args, **kwargs)
