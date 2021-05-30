# Los enlaces que manejo de las paginas a las que acceden

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('registro/', views.registerPage, name ='registro'),
    path('login/', views.loginPage, name ='login'),
    path('logout/', views.logoutUser, name ='logout'),

    path('', views.home, name = 'inicio'),
    path('user/', views.userPage, name ='pagina-usuario'),
    path('cuenta/', views.accountSettings, name ='cuenta'),
    path('productos/', views.products, name ='productos'),
    path('clientes/<str:pk_test>/', views.customer, name = 'clientes'),

    path('crearPedido/<str:pk>/',views.createOrder, name = 'crearPedido'),
    path('actualizarPedido/<str:pk>/',views.updateOrder, name = 'actualizarPedido'),
    path('eliminarPedido/<str:pk>/',views.deleteOrder, name = 'eliminarPedido'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="plantillas/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="plantillas/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="plantillas/password_reset_form.html"),
     name="password_reset_confirm"),

    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="plantillas/password_reset_done.html"), 
        name="password_reset_complete"),

]
