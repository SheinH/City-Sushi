from django.urls import path

from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('orderplaced/', views.orderPlaced, name='orderplaced'),
    path('register/', views.customerRegister, name='register'),
    # path('customer/login/', views.customerLogin, name='login'),
    path('profile/', views.customerProfile, name='profile'),
    path('customer/create/', views.createCustomer, name='ccreate'),
    path('user/update/<int:id>/', views.updateCustomer, name='cupdate'),
    # path('checkout/', views.checkout, name='checkout')
]
