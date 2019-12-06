from django.urls import include,path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
    path('menu', views.menu, name='menu'),
    path('orderplaced/',views.orderplaced)
]
