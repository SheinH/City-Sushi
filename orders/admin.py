# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Customer)
admin.site.register(Visitor)
admin.site.register(PaymentInfo)
admin.site.register(Dish)
admin.site.register(Review)
