from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LogIn, name='login'),
    path('books/', views.Books, name='books'),
    path('cargo/',views.Cargos,name='cargo'),
    path('bill/',views.Bills,name='bill'),
    path('userinfo/',views.userInfo, name='userinfo')
]
