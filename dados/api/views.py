from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def VerificaUsuarioExiste(request):
    try:
        info = request.data
        email_cadastrado = usuario.objects.filter(email=info['email']).first()
        if email_cadastrado:
            return JsonResponse({'mensagem': 'Este email já está cadastrado'}, status=200)
        else:
            CadastraUsuario(request)
            return JsonResponse({'mensagem': 'Usuário não cadastrado'}, status=200)
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro na verificação de existência do email: {str(e)}'}, status=500)

def CadastraUsuario(request):
    try:
        info = request.data
        usuario_obj = usuario.objects.create(
            nome=info['nome'],
            email=info['email'],
            senha=info['senha'],
            endereco=info['endereco'],
            celular=info['celular'],
        )
        return JsonResponse({'mensagem': 'Cadastro do usuário efetuado', 'usuario_id': usuario_obj.id}, status=201)
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro ao cadastrar usuário no banco: {str(e)}'}, status=500)

@api_view(['POST'])
def VerificaLogin(requests):
    try:
        LoginUsuario = False
        info = requests.data
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
    
