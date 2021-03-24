from django.db import models

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length = 200, null = True)
    telefono = models.CharField(max_length = 200, null = True)
    email = models.CharField(max_length = 200, null = True)
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
