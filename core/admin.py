from django.contrib import admin

from core.models import Tenant, Domain, Product

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Domain)
admin.site.register(Product)
