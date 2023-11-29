from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view


def VerificaUsuarioExiste(request):
    try:
        CadastraUsuario = True
        info = request.data
        EmailCadastrado = usuario.objects.filter(email=info['email']).first()
        if EmailCadastrado:
            return JsonResponse({'mensagem': 'Este email já está cadastrado'},True)
        else:
            return CadastraUsuario
    except: 
        raise Exception("Erro na verificação de existencia do email")

@api_view(['POST'])
def CadastraUsuario(request):
    try:
        info = request.data
        CadastraUsuario = True
        usuario.objects.create(
            nome=info['nome'],
            email=info['email'],
            senha=info['senha'],
            endereco=info['endereco'],
            celular=info['celular'],
        )   
        return JsonResponse({'Cadastro do Usuario efetuado',CadastraUsuario})
    except:
        CadastraUsuario = False
        raise Exception("Erro ao cadastra usuario no banco",CadastraUsuario)

@api_view(['POST'])
def VerificaLogin(request):
    try:
        LoginUsuario = False
        info = request.data
        UsuarioExiste = usuario.objects.filter(email=info['email'])
        if UsuarioExiste:
            if UsuarioExiste.senha == info['senha']:
                LoginUsuario = True
                return JsonResponse({"mensagem:" "Login efetuado",LoginUsuario})
            else:
                return JsonResponse({'mensagem:' 'Email cadastrado porém senha esta errada',LoginUsuario})
        else:
            return JsonResponse({"mensagem:" "Email não cadastrado no banco de dados",LoginUsuario})
    except:
        raise Exception("Erro ao verificar login",LoginUsuario)
    
