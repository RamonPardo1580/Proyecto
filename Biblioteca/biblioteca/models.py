# Los modelos son como mis plantillas para crear mis tablas
# de bases de datos desde Django sin necesidad de crear una como tal
# e importarla a la aplicaion web
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    user = models.OneToOneField(User, null = True, blank = True, on_delete = models.CASCADE)
    nombre = models.CharField(max_length = 200, null = True)
    telefono = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
    imagen_perfil = models.ImageField(default = "profile1.png", null = True , blank = True)
    fecha_creada = models.DateTimeField(auto_now_add = True, null = True)


    def __str__(self):
        return self.nombre

class Tag(models.Model):
    nombre = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    CATEGORIA = (
        ('Libros','Libros'),
        ('Novelas', 'Novelas'),
        ('Historietas', 'Historietas'),
        ('Periodicos', 'Periodicos'),
        )

    nombre = models.CharField(max_length = 200, null = True)
    precio = models.FloatField(null = True)
    categoria = models.CharField(max_length = 200, null = True, choices = CATEGORIA)
    descripccion = models.CharField(max_length = 200, null = True, blank = True)
    fecha_creada = models.DateTimeField(auto_now_add = True, null = True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.nombre

class  Pedido(models.Model):
    ESTATUS = (
        ('Pendiente','Pendiente'),
        ('En camino', 'En camino'),
        ('Entregado', 'Entregado'),
    )

    cliente = models.ForeignKey(Cliente, null = True, on_delete = models.SET_NULL)
    producto = models.ForeignKey(Producto, null = True, on_delete = models.SET_NULL)
    fecha_creada = models.DateTimeField(auto_now_add = True, null = True)
    estatus = models.CharField(max_length = 200, null = True, choices = ESTATUS)
    note = models.CharField(max_length = 1000, null = True)

    def __str__(self):
        return self.producto.nombre
