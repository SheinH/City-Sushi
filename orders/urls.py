from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('main/', views.main, name='main'),
    path('orderplaced/', views.orderPlaced, name='orderplaced'),
    path('register/', views.customerRegister, name='register'),
    # For actual customers in model
    path('cregister/', views.realCustomerRegister, name='cregister'),
    path('profile/', views.customerProfile, name='profile'),
    path('profile/addpayment', views.add_payment_form, name='addpayment'),
    path('customer/create/', views.createCustomer, name='ccreate'),
    path('user/update/<int:id>/', views.updateCustomer, name='cupdate'),
    # path('checkout/', views.checkout, name='checkout')
]
