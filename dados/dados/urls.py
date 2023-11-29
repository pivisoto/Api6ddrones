from django.contrib import admin
from django.urls import path , include
from api.models import *
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verifica_usuario_existe/',views.VerificaUsuarioExiste)
]
