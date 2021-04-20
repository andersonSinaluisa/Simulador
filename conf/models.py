from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class ClaseModelo(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_crea = models.IntegerField(blank=True,
                                       null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_modifica = models.IntegerField(blank=True,
                                           null=True)

    class Meta:
        abstract = True


class Usuarios(AbstractUser):
    img_perfil = models.ImageField(upload_to='perfil_img',
                                   null=True,
                                   blank=True)
    telefono = models.CharField(max_length=20, null=True)

# Modelos para asignacion de permisos


class UsuariosGrupos(models.Model):
    usuarios = models.ForeignKey(Usuarios, models.DO_NOTHING)
    group = models.ForeignKey(Group, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'conf_usuarios_groups'
        unique_together = (('usuarios', 'group'),)


class GruposPermisos(models.Model):
    group = models.ForeignKey(Group, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)
