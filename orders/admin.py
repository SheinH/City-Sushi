from django.contrib import admin

# Register your models here.

from .models import *

# We will need to tidy up on the .models we imported.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(Review)