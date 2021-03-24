from django.urls import path

from . import views


urlpatterns = [
    path('', views.home),
    path('productos/', views.products),
    path('clientes/<str:pk_test>/', views.customer),
]
