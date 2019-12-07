# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(Restaurant)
admin.site.register(Manager)
admin.site.register(Sales)
admin.site.register(Cook)
admin.site.register(Delivery)
admin.site.register(Inventory)