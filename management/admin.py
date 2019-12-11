# Register your models here.
from django.contrib import admin

from orders.models import PaymentInfo, ShippingAddress
from .models import *

admin.site.register(Restaurant)
admin.site.register(Manager)
admin.site.register(Sales)
admin.site.register(Cook)
admin.site.register(Delivery)
admin.site.register(Inventory)
admin.site.register(PaymentInfo)
admin.site.register(ShippingAddress)
