# Create your views here.
from django.shortcuts import render

from .models import Dish


# Homepage
def index(request):
    return render(request, 'orders/index.html', {})


def menu(request):
    context = {'items' : Dish.objects.all()}
    print(Dish.objects.all())
    return render(request, 'orders/menu.html', context)

