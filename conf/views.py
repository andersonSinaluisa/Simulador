from django.shortcuts import redirect, render
from django.urls import reverse_lazy

# Create your views here.
from django.views.generic import CreateView, ListView
from .models import Usuarios, UsuariosGrupos, GruposPermisos
from .forms import RegistroForm, LoginForm
from .backend import EmailBackend
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class CrearUsuario(CreateView):
    model = Usuarios
    template_name = 'registro.html'
    success_url = reverse_lazy('conf:login')
    form_class = RegistroForm

    def post(self, request):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            obj = form.save()
            obj.password = make_password(obj.password)
            obj.is_superuser = False
            obj.is_staff = False
            obj.save()
            grupo = Group.objects.filter(name='USUARIOS').first()
            UsuariosGrupos.objects.create(usuarios=obj, group=grupo)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


def loginUsuario(request):
    template_name = "login.html"
    form = LoginForm

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = EmailBackend.authenticate(
            EmailBackend,
            request,
            username,
            password
        )
        if user is not None:
            if not user.is_active:
                return render(
                    request,
                    template_name,
                    {
                        'form': form,
                        'mensaje': 'Usuario Inactivo'
                    }
                )
            else:
                login(request, user)
                return redirect("ques:index")
        else:
            return render(
                request,
                template_name,
                {
                    'form': form,
                    'mensaje': 'Usuario y/o contraseña incorrecta'
                }
            )
    if request.user.is_authenticated:
        return redirect('ques:index')
    return render(request, template_name, {'form': form})


class GrupoList(ListView):
    model = GruposPermisos
    context_object_name = 'obj'
    template_name = 'grupos.html'


