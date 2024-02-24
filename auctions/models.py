from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Grupo(models.Model):
    nombre = models.CharField(max_length=64)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grupos_creados")
    miembro= models.ManyToManyField(User, blank=True, related_name="grupos" )


class Archivos(models.Model):
    publicador= models.ForeignKey(User, on_delete=models.CASCADE, related_name="archivos_de_usuario")
    grupo= models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="archivos_de_grupo")
    nombre = models.CharField(max_length=64)
    archivo = models.FileField(upload_to="media")