from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *

def home(request):
    pedidos = Pedido.objects.all()
    cliente = Cliente.objects.all()

    total_clientes = cliente.count()
    total_pedidos = pedidos.count()

    entregado = pedidos.filter( estatus ='Entregado').count()
    pendiente = pedidos.filter(estatus = 'Pendiente').count()

    contexto = {'pedido':pedidos, 'cliente':cliente , 'total_pedidos': total_pedidos,
                'entregado': entregado, 'pendiente':pendiente}
    return render(request, 'plantillas/inicio.html', contexto)

def products(request):
    productos = Producto.objects.all()
    return render(request, 'plantillas/productos.html', {'producto':productos})

def customer(request, pk_test):
    clientes = Cliente.objects.get(id = pk_test)
    pedidos = clientes.pedido_set.all()
    total_pedido = pedidos.count()
    contexto = {'clientes':clientes, 'pedidos':pedidos ,'total_pedido':total_pedido}
    return render(request, 'plantillas/clientes.html',contexto)
