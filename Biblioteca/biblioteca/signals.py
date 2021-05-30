from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Cliente

def perfil_cliente(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='cliente')
		instance.groups.add(group)
		Cliente.objects.create(
			user=instance,
			nombre=instance.username,
			)
		print('Perfil creado!')

post_save.connect(perfil_cliente, sender=User)
