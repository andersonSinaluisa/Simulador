from django.urls import path
from .views import index, PreguntasList, Upload_file, cargar_preguntas,marcar_respuesta, RespuestasCreate


urlpatterns = [
    path('', index, name='index'),
    path('preguntas/', PreguntasList.as_view(), name='preguntas'),
    path('subir-preguntas/', Upload_file.as_view(), name='subir_preguntas'),
    path('cargar-preguntas/',cargar_preguntas,name='cargar_preguntas'),
    path('nueva-repuesta/',RespuestasCreate.as_view(),name='nueva_repuesta'),
    path('marcar-respuesta/',marcar_respuesta,name = 'marcar_respuesta')

]
