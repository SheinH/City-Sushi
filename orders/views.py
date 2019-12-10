from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerSignUpForm, CustomerForm, ReviewForm
# Create your views here.
from django.shortcuts import render
from .models import Visitor, Customer, Payment_Info, Dish, Review


# Homepage
def index(request):
    return render(request, 'orders/index.html', {})


def menu(request):
    context = {'items': Dish.objects.all()}
    print(Dish.objects.all())
    return render(request, 'orders/menu.html', context)


def orderPlaced(request):
    print(dict(request.POST))

    def get_dish(id):
        return Dish.objects.get(pk=id)

    orders = {get_dish(k): int(v[0]) for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}
    context = {'orders': orders}
    return render(request, 'orders/orderplaced.html', context)


# logout for both users (restaurants and regular customers)
def logout(request):
    logout(request)
    return redirect("login")


# Customer side of things

# Register customer account
def customerRegister(request):
    form = CustomerSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.is_customer = True
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("ccreate")
    return render(request, 'orders/signup.html', context={'form': form})


# Let customers log in
def customerLogin(request):
    if request.method == "POST":
        username = request.post['username']
        password = request.post['password']
        user = authenticate(username=username, password=password)

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
# turn user into customer
# build context dictionary { 'visitor' : visitor }
# return render( request, 'orders/profile.html', context)

def customerProfile(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    info = Payment_Info.objects.filter(customer=customer)
    context = {'v': customer, 'i': info}
    print(context)
    # context = {'visitor': user}
    return render(request, 'orders/profile.html', context)


# create the customer profiles
def createCustomer(request):
    form = CustomerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return render(request, 'orders/profile_form.html', context={'form': form, 'title': "Complete Profile"})


# update any details on customer profiles
def updateCustomer(request):
    form = CustomerForm(request.POST or None, instance=request.user.customer)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'orders/profile_form.html', context={'form': form, 'title': "Update Profile"})

# need to finish checkout function
