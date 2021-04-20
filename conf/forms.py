from django import forms
from .models import Usuarios
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ValidationError


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Usuarios
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'telefono'
        ]
        labels = {
            'username': 'Nombre usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo',
            'telefono': 'Telefono',
            'password': 'Contraseña'
        }
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellidos'}),
            'email': forms.TextInput(attrs={'placeholder': 'Correo'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Telefono'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
        }

    def clean(self):
        cd = self.cleaned_data
        email = cd.get("email")
        username = cd.get("username")
        password = cd.get("password")
        if Usuarios.objects.filter(username=username):
            raise ValidationError("Este Nombre de usuario ya está en uso")
        if Usuarios.objects.filter(email=email):
            raise ValidationError("Este Correo ya está en uso")
        if len(password) < 8:
            raise ValidationError(
                "La contraseña debe tener mas de 8 carácteres")
        return cd

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
