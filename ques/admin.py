from django.contrib import admin
from .models import Quizz, QuizzUsuario, Pregunta, Respuestas,File
# Register your models here.
admin.site.register(Quizz)
admin.site.register(QuizzUsuario)
admin.site.register(Pregunta)
admin.site.register(Respuestas)
admin.site.register(File)