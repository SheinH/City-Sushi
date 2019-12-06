from django.shortcuts import render

# Create your views here.
import django.views.generic
from django.views import generic
from .models import Dish
from django.shortcuts import render

# Homepage
def index(request):
	return render(request, 'orders/index.html', {})


def menu(request):
    context = {'items' : Dish.objects.all()}
    print(Dish.objects.all())
    return render(request, 'orders/menu.html', context)

