from django.contrib import admin

from core.models import Customer, Domain, Product

# Register your models here.
admin.site.register(Customer)
admin.site.register(Domain)
admin.site.register(Product)
