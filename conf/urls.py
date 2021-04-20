from django.urls import path
from .views import CrearUsuario, loginUsuario, GrupoList
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('registro/', CrearUsuario.as_view(), name='registro'),
    path('', loginUsuario, name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'
         ),
    path('grupos/', GrupoList.as_view(), name='grupos')
]
