from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
# Create your views here.
from django.shortcuts import render

from .forms import CustomerSignUpForm, CustomerForm, PaymentForm, CustomerRegistrationForm
from .models import Customer, Dish, Order, OrderItem, PaymentInfo


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

    customer = Customer.objects.get(user=request.user)

    orders = {get_dish(k): int(v[0]) for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}

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
        f.customer = customer
        if f.is_valid():
            f.save()
            messages.success(request, 'Saved payment info')
            return render(request, 'orders/profile.html', {'form': f})
    else:
        f = CustomerSignUpForm()
    return render(request, 'orders/register.html', {'form': f})


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
            b = User.objects.create_user(
                username=f.cleaned_data['username'],
                password=f.cleaned_data['password'],
                email=a.email
            )

            b.save()
            a.user = b
            a.save()
            messages.success(request, 'Account created successfully')
            return render(request, 'orders/cregister.html', {'form': f})
    else:
        f = CustomerRegistrationForm()
    return render(request, 'orders/cregister.html', {'form': f})


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
    info = PaymentInfo.objects.filter(customer=customer)
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
