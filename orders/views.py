from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerSignUpForm, CustomerForm, RestuarantForm, ReviewForm
# Create your views here.
import django.views.generic
from django.views import generic
from .models import Dish
from django.shortcuts import render

# Homepage
def index(request):
	return render(request, 'orders/index.html', context)


def menu(request):
    context = {'items' : Dish.objects.all()}
    print(Dish.objects.all())
    return render(request, 'orders/menu.html', context)

def orderPlaced(request):
	return render(request, 'orders/orderPlaced.html', context)

# logout for both users (restaurants and regular customers)
def Logout(request):
	if request.user.is_restaurant:
		logout(request)
		return redirect("rlogin")
	else:
		logout(request)
		return redirect("login")

# Customer side of things

# Register customer account
def customerRegister(request):
	form = CustomerSignUpForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit = False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.is_customer = True
		user.set_password(password)
		user.save()
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return rredirect("ccreate")
	return render(request, 'orders/signup.html', context = {'form': form})


# Let customers log in
def customerLogin(request):
	if request.method == "POST":
		username = request.post['username']
		password = request.post['password']
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect("profile")
			else:
				return render(request, 'orders/login.html', {'error message': 'Invalid Username and Password'})
		else:
			return render(request, 'orders/login.html', {'error message': 'Invalid Username and Password'})
	return render(request, 'orders/login.html')

# view customer profiles based on ids
def customerProfile(request, pk = None):
	if pk:
		user = User.objects.get(pk = pk)
	else:
		user = request.user
	return render(request, 'orders/profile.html', {'user':user})