from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView, ListView
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
import json

from .models import Pregunta, File, Respuestas, Quizz
from .forms import NuevoArchivo, RespuestasForm
from django.urls import reverse_lazy
import os
import xlrd
# Create your views here.


class RespuestasCreate(CreateView):
    model = Respuestas
    form_class = RespuestasForm
    template_name = 'nueva_respuesta.html'
    success_url = reverse_lazy('ques:nueva_repuesta')

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')


class PreguntasList(ListView):
    model = Pregunta
    template_name = 'preguntas.html'
    context_object_name = 'a'

    def get_context_data(self, **kwargs):
        contexto = {}
        lista = Pregunta.objects.filter(estado=True)
        final = []
        val = False
        for i in lista:
            respuestas = Respuestas.objects.filter(id_pregunta=i.id_pregunta)
            if respuestas.count()>=4:
                for a in respuestas:
                    if a.correcta == False:
                        val = True
                    
                if val:
                    final.append((i, respuestas))
                    val = False
        contexto['lista'] = final
        return contexto


def cargar_preguntas(request):
    if request.method == 'POST':
        quizz = Quizz.objects.filter(estado=True).first()
        if quizz:
            archivo = File.objects.all().last()
            workbook = xlrd.open_workbook(
                ('media/{0}').format(archivo.archivo))
            lista = []
            count = 0
            pregunta = None
            for worksheet in workbook.sheets():
                for i in range(1, worksheet.nrows):
                    count = count + 1
                    array = worksheet.row_values(rowx=i)
                    for a in array:
                        numero = 0
                        if type(a) is float or type(a) is int:
                            numero = a
                        if a != '' and type(a) is str:
                            if a.endswith("?") or a.startswith("¿"):
                                pregunta = Pregunta.objects.create(
                                    descripcion=a, estado=True, puntos=numero)
                            else:
                                if pregunta:
                                    Respuestas.objects.create(descripcion=a, id_pregunta=pregunta, estado=True, correcta=False)
                    if count == 5:
                        count = 0
                        pregunta = None

        return redirect(to=reverse_lazy('ques:preguntas'))


def marcar_respuesta(request):
    if request.method == 'POST':
        
        json_data = json.loads(request.POST['lista'])

        for i in json_data:
            a = Respuestas.objects.get(id_respuesta=int(i))
            
            a.correcta = True
            a.save()
        return JsonResponse(
                {'content': 'ok'}
            )


class Upload_file(View):
    model = File
    form_class = NuevoArchivo
    template_name = 'cargar_preguntas.html'
    success_url = reverse_lazy('ques:preguntas')

    def handle_uploaded_file(self, f):
        with open('media/{0}'.format(str(f)), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self,  request, *args, **kwargs):
        form = NuevoArchivo(self.request.POST, self.request.FILES)
        if form.is_valid():
            self.handle_uploaded_file(self.request.FILES['file'])
        return render(request, self.template_name, {'form': form})
