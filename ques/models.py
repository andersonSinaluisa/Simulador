from django.db import models
# Create your models here.
from conf.models import Usuarios


class Quizz(models.Model):
    id_quizz = models.AutoField(primary_key=True)
    estado = models.BooleanField()
    nombre = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Quizz'
        verbose_name_plural = 'Quizz'


class QuizzUsuario(models.Model):
    id_quizz_usuario = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuarios, on_delete=models.CASCADE, related_name='fk_usuario_quizz')
    puntaje = models.DecimalField(decimal_places=2, max_digits=6)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'QuizzUsuario'
        verbose_name_plural = 'QuizzUsuarios'


class Pregunta(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=400)
    estado = models.BooleanField()
    puntos = models.DecimalField(decimal_places=2, max_digits=6)
    id_quizz = models.ManyToManyField(
        Quizz, related_name='fk_quizz_pregunta')

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return str(self.id_pregunta) +" "+self.descripcion


class Respuestas(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    descripcion = models.TextField(max_length=400)
    id_pregunta = models.ForeignKey(
        Pregunta, on_delete=models.CASCADE,
        related_name='fk_respuesta_pregunta', null=True)
    estado = models.BooleanField()
    correcta = models.BooleanField()

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'


class File(models.Model):
    id_file = models.AutoField(primary_key=True)
    archivo = models.FileField(upload_to='')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'