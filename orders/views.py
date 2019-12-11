import urllib

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render

from .forms import *
from .models import Customer, Dish, Order, OrderItem, PaymentInfo, Address, Review
from .models import Restaurant
from django.forms.models import model_to_dict


# Homepage
def index(request):
    return render(request, 'orders/index.html', {})


def menu(request):
    context = {'items': Dish.objects.all()}
    print(Dish.objects.all())
    return render(request, 'orders/menu.html', context)


def main(request):
    context = {'r': Restaurant.objects.all()}
    print(Restaurant.objects.all())
    return render(request, 'orders/main.html', context)


def review(request, id):
    if request.method == 'POST':
        f = ReviewForm(request.POST)
        if f.is_valid():
            rev: Review = f.save(commit=False)
            customer = Customer.objects.get(user=request.user)
            rev.dish = Dish.objects.get(pk=id)
            rev.reviewer = request.user
            rev.save()
            messages.success(request, 'Review added')
            return render(request, 'orders/review.html', {'form': f})
    else:
        f = ReviewForm()
    return render(request, 'orders/review.html', {'form': f})


def orderPlaced(request):
    print(dict(request.POST))

    def get_dish(id):
        return Dish.objects.get(pk=id)

    customer = Customer.objects.get(user=request.user)

    orders = {get_dish(k): int(v[0]) for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and int(v[0]) != 0}

    ord = Order(vis=customer)
    ord.save()
    for k, v in orders.items():
        ord_item = OrderItem(dish=k, quantity=v, order=ord)
        ord_item.save()
    context = {'orders': orders}
    return render(request, 'orders/orderplaced.html', context)


# logout for both users (restaurants and regular customers)
def logout(request):
    logout(request)
    return redirect("login")

def cookView(request):
    items = OrderItem.objects.filter(is_cooked=True)
    return render(request,'orders/cookpage.html',{'items' : items})
# Customer side of things

# Register customer account
# def customerRegister(request):
#     form = CustomerSignUpForm(request.POST or None)
#     if form.is_valid():
#         user = form.save(commit=False)
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user.is_customer = True
#         user.set_password(password)
#         user.save()
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect("ccreate")
#     return render(request, 'orders/signup.html', context={'form': form})

# Better registration form
def add_payment_form(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        f = PaymentForm(request.POST)
        if f.is_valid():
            a = f.save(commit=False)
            a.customer = customer
            a.save()
            messages.success(request, 'Saved payment info')
            return redirect('orders:addpayment')
    else:
        f = PaymentForm()
    return render(request, 'orders/addpayment.html', {'form': f})


def customerRegister(request):
    if request.method == 'POST':
        f = CustomerSignUpForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'orders/register.html', {'form': f})
    else:
        f = CustomerSignUpForm()
    return render(request, 'orders/register.html', {'form': f})


def realCustomerRegister(request):
    if request.method == 'POST':
        f = CustomerRegistrationForm(request.POST)
        if f.is_valid():
            a = f.save(commit=False)
            addr = Address(
                street_addr=f.cleaned_data['address'],
                zip_code=f.cleaned_data['zip_code'],
                city=f.cleaned_data['city']
            )
            addr.save()
            b = User.objects.create_user(
                username=f.cleaned_data['username'],
                password=f.cleaned_data['password'],
                email=a.email
            )
            b.save()
            a.user = b
            a.address = addr
            a.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'orders/cregister.html', {'form': f})
    else:
        f = CustomerRegistrationForm()
    return render(request, 'orders/cregister.html', {'form': f})


def to_table(items, start_col=0):
    arr = [model_to_dict(x) for x in items]
    headers = [x for x in arr[0]]
    rows = [x.values() for x in arr]
    return {'headers': headers, 'rows': rows}


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
    addr = urllib.parse.quote(str(customer.address))
    info = PaymentInfo.objects.filter(customer=customer)
    # context = {'v': customer, 'i': info, 'location': addr}
    orders = Order.objects.filter(vis=customer)
    context = {'v': customer, 'i': info, 'location': addr, 'orders': orders}
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
