# Esta es la pestaña de vistas aqui es donde se renderiza todo lo
# que realizan las paginas web y se renderizan

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
# Create your views here.
from .models import *
from .forms import PedidoForma, CrearUsuarioForma, clienteForma
from .filters import PedidosFiltro
from .decorators import unauthenticated_user, allowed_users, admin_only

# Registar Usuario
@unauthenticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CrearUsuarioForma(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Se creo una cuenta para ' + username)

            return redirect('login')

    contexto = {'form':form}
    return render(request, 'plantillas/registro.html', contexto)

#Pagina de Login
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username , password = password)

        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.info(request, 'El Usuario o la contraseña son incorrectos')

    contexto = {}
    return render(request, 'plantillas/login.html', contexto)

# funcion desconectar
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url = 'login') #Restringe la entrada sin logear
@admin_only
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


# Muestra en la pagina del usuario
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['cliente'])
def userPage(request):
    pedidos = request.user.cliente.pedido_set.all()

    total_pedidos = pedidos.count()
    entregado = pedidos.filter( estatus ='Entregado').count()
    pendiente = pedidos.filter(estatus = 'Pendiente').count()
    print('Pedidos',pedidos)

    contexto ={'pedidos':pedidos, 'total_pedidos': total_pedidos,
                'entregado': entregado, 'pendiente':pendiente}
    return render(request, 'plantillas/user.html', contexto)

# configuracion del perfil del usuario
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['cliente'])
def accountSettings(request):
    cliente = request.user.cliente
    form = clienteForma(instance = cliente)

    if request.method == 'POST':
        form = clienteForma(request.POST, request.FILES, instance = cliente)
        if form.is_valid():
            form.save()

    contexto = {'form': form}
    return render(request, 'plantillas/perfil_configuracion.html', contexto )

# Funcion de productos existentes
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['Admin'])
def products(request):
    productos = Producto.objects.all()
    return render(request, 'plantillas/productos.html', {'producto':productos})

# Funcion para pagina de clientes
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['Admin'])
def customer(request, pk_test):
    clientes = Cliente.objects.get(id = pk_test)

    pedidos = clientes.pedido_set.all()
    total_pedido = pedidos.count()

    filtrar = PedidosFiltro(request.GET, queryset = pedidos)
    pedidos = filtrar.qs

    contexto = {'clientes':clientes, 'pedidos':pedidos ,'total_pedido':total_pedido, 'filtrar': filtrar}
    return render(request, 'plantillas/clientes.html',contexto)

# Funcion para crear un pedido y asignarselo a un cliente
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['Admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Cliente,Pedido, fields = ('producto', 'estatus'), extra = 5)
    cliente = Cliente.objects.get(id = pk)
    formset = OrderFormSet(queryset = Pedido.objects.none(),instance = cliente)
    #form = PedidoForma(initial={'cliente':cliente}) #trabajando en esta linea
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = PedidoForma(request.POST) # esta linea
        formset = OrderFormSet(request.POST, instance = cliente)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    contexto = {'form': formset}
    return render(request, 'plantillas/pedidos_forma.html', contexto)

# Funcion para actualizar el pedido de un cliente
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['Admin'])
def updateOrder(request, pk):
    ped = Pedido.objects.get(id = pk)
    form = PedidoForma(instance = ped)

    if request.method == 'POST':
        form = PedidoForma(request.POST, instance = ped)
        if form.is_valid():
            form.save()
            return redirect('/')
    contexto = {'form': form}
    return render(request, 'plantillas/pedidos_forma.html', contexto)

# Funcion para elimar un pedido de un cliente
@login_required(login_url = 'login')
@allowed_users(allowed_roles = ['Admin'])
def deleteOrder(request, pk):
    ped = Pedido.objects.get(id = pk)
    if request.method == "POST":
        ped.delete()
        return redirect('/')

    contexto = {'item': ped}
    return render(request, 'plantillas/eliminar.html', contexto)
