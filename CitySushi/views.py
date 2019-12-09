from django.shortcuts import render
from django.shortcuts import redirect

def index(request):
    if request.user.is_authenticated:
        response = redirect('/orders/menu')
        return response
    else:
        response = redirect('/accounts/login')
        return response
