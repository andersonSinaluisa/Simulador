from django import forms
from .models import File, Respuestas
from django.forms import ValidationError


class NuevoArchivo(forms.Form):
    file = forms.FileField(
        required=True,
        widget=forms.FileInput(
            attrs={'class': 'form-control file-upload-info', 'accept': '.xlsx'}
        )
    )


class RespuestasForm(forms.ModelForm):
    class Meta:
        model = Respuestas
        fields = '__all__'

    def clean(self):
        cd = self.cleaned_data
        descripcion = cd.get("descripcion")
        id_pregunta = cd.get("id_pregunta")
        correcta = cd.get("correcta")
        respuesta = Respuestas.objects.filter(id_pregunta=id_pregunta).count()
        if respuesta >= 4:
            raise ValidationError("Esta pregunta ya tiene las 4 repuestas")
        respuesta_correcta = Respuestas.objects.filter(
            id_pregunta=id_pregunta, correcta=True).count()
        if correcta and respuesta_correcta:
            raise ValidationError("Esta pregunta ya tiene respuesta correcta")
        des_validate = Respuestas.objects.filter(
            descripcion=descripcion, id_pregunta=id_pregunta)
        if des_validate:
            raise ValidationError("Esta respuesta ya esta creada")
        return cd

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
