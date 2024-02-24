from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass


class Grupo(models.Model):
    nombre = models.CharField(max_length=64, unique=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grupos_creados")
    miembro= models.ManyToManyField(User, blank=True, related_name="grupos" )



# esto para crear una carpeta a cada usuario y usarlo en el "upload_to" en el modelo del archivo
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.publicador.id, filename)

class Archivos(models.Model):
    publicador= models.ForeignKey(User, on_delete=models.CASCADE, related_name="archivos_de_usuario")
    grupo= models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="archivos_de_grupo")
    nombre = models.CharField(max_length=64)
    archivo = models.FileField(upload_to=user_directory_path)