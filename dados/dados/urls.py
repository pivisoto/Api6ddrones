from django.contrib import admin
from django.urls import path , include
from api.models import *
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('verifica_usuario_existe/',views.VerificaUsuarioExiste),
    path('verificaLogin/',views.VerificaLogin),
    path('exibeInfo/',views.ExibeInfo),
    path('exibeOrg/',views.ExibeOrg),
    path('concedeAdmOrg/',views.ConcedeAdmOrg),
    path('removeAdmOrg/',views.RemoveAdmOrg),
    path('concedeAdmInter/',views.ConcedeAdmInter),
    path('removeAdmInter/',views.RemoveAdmInter),
]
