from django.contrib import admin
from home.models import ProductModel , OrderModel
# Register your models here.

from django.contrib.auth.models import Group


admin.site.register(ProductModel)
admin.site.register(OrderModel)


customer_group,created = Group.objects.get_or_create(name = 'customer')
owner_group , created = Group.objects.get_or_create(name='owner')

