# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Visitor)
admin.site.register(PaymentInfo)
admin.site.register(Dish)
admin.site.register(Review)
admin.site.register(Address)
admin.site.register(Restaurant)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cook)
admin.site.register(Sales)
admin.site.register(Deliverer)