from .models import *
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password


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
def VerificaLogin(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            senha = info['senha']
            if usuario_existe.senha == senha:
                return JsonResponse({"mensagem": "Login efetuado"}) 
            else:
                raise Exception({'mensagem': 'Email cadastrado, mas a senha está incorreta'})
        else:
            raise Exception({"mensagem": "Email não cadastrado no banco de dados"})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao verificar login","error": str(e)}, status=401)

@api_view(['GET'])
def ExibeInfo(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        nome = usuario_existe.nome
        email = usuario_existe.email 
        celular = usuario_existe.celular 
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg').first()
        organizacao_nome = organizacao_busca['nomeOrg']
        if organizacao_busca:
            ResponseData = {
                'nome': nome,
                'email' : email,
                'celular' : celular,
                'organizacao_nome' : organizacao_nome
            }
            print(nome,email,celular,organizacao_nome)
        else:
            ResponseData = {
                'nome': nome,
                'email' : email,
                'celular' : celular,
            }
            print(nome,email,celular)
        return JsonResponse(ResponseData)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar dados de usuario","error": str(e)}, status=500)
    
@api_view(['GET'])
def ExibeOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg','cpf_cnpj','idOrganizador').first()
        organizacao_nome = organizacao_busca['nomeOrg']
        organizacao_cpf = organizacao_busca['cpf_cnpj']
        organizacao_id = organizacao_busca['idOrganizador']
        ResponseData = {
                'razao_social': organizacao_nome,
                'cpf_cnpj' : organizacao_cpf,
                'id' : organizacao_id,
        }
        return JsonResponse(ResponseData)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar dados de organização","error": str(e)}, status=500)