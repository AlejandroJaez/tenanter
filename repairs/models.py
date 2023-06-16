from django.contrib.auth import get_user_model
from django.db import models
from easy_tenants import get_current_tenant
from easy_tenants.models import TenantManager

from config import settings
from core.models import Tenant
field_name = settings.EASY_TENANTS_TENANT_FIELD
# Create your models here.
User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=255)


class Issues(models.Model):
    name = models.CharField(max_length=255)


class PhoneModel(models.Model):
    name = models.CharField(max_length=255)


class RepairOrder(models.Model):
    serial_number = models.CharField(max_length=16)
    date_crated = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    phone_model = models.ForeignKey(PhoneModel, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)

    objects = TenantManager()

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        """Set tenant field on save"""
        if getattr(self, "tenant_id") is None:
            setattr(self, field_name, get_current_tenant())
        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    date_created = models.DateTimeField()
    order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE)
