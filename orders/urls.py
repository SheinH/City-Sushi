from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('orderplaced/', views.orderPlaced),
    path('customer/register/', views.customerRegister, name='register'),
    path('customer/login/', views.customerLogin, name='login'),
    path('customer/profile/', views.customerProfile, name='profile'),
    path('customer/create/', views.createCustomer, name='ccreate'),
    path('user/update/<int:id>/', views.updateCustomer, name='cupdate'),
    path('logout/', views.Logout, name='logout'),
    path('checkout/', views.checkout, name='checkout')
]
