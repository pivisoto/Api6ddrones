from django.contrib import admin
from django.urls import path , include
from api.models import *
from api import views

urlpatterns = [
    path('admin/',admin.site.urls),
    path('verifica_usuario_existe/',views.VerificaUsuarioExiste),
    path('verificaLogin/',views.VerificaLogin),
    path('atualizaUsuario/',views.AtualizaUsuario),
    path('exibeInfo/',views.ExibeInfo),
    path('criarOrg/',views.CriarOrg),
    path('defineIdOrganizador/',views.DefineIdOrganizador),
    path('removePessoaOrganizacao/',views.RemovePessoaOrganizacao),
    path('atualizaOrg/',views.AtualizaOrg),
    path('exibeOrg/',views.ExibeOrg),
    path('criarProjeto/',views.CriarProjeto),
    path('atualizaProjeto/',views.AtualizaProjeto),
    path('exibeProjeto/',views.ExibeProjeto),
    path('defineIdProjeto/',views.DefineIdProjeto),
    path('removePessoaProjeto/',views.RemovePessoaProjeto),
    path('concedeAdmOrg/',views.ConcedeAdmOrg),
    path('removeAdmOrg/',views.RemoveAdmOrg),
    path('concedeAdmInter/',views.ConcedeAdmInter),
    path('removeAdmInter/',views.RemoveAdmInter),
    path('verificaAdmGeral/',views.VerificaAdmGeral),
    path('verificaAdmOrg/',views.VerificaAdmOrg),
    path('verificaAdmInter/',views.VerificaAdmInter),
    path('recebeEmail/',views.RecebeEmail),
    path('atualizaSenha/',views.AtualizaSenha),
    path('exibeTodosUsuarios/',views.ExibeTodosUsuarios),
    path('exibeTodasOrganizacoes/',views.ExibeTodasOrganizacoes),
    path('exibeTodosProjetos/',views.ExibeTodosProjetos),
    path('apagaOrg/',views.ApagaOrg),
    path('apagaProjeto/',views.ApagaProjeto),
]
