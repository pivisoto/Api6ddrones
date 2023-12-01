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
            return JsonResponse({'mensagem': 'Usuário não cadastrado'})
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro na verificação de existência do email: {str(e)}'}, status=500)

def CadastraUsuario(request):
    try:
        info = request.data
        usuario_obj = usuario.objects.create(
            nome=info['nome'],
            email=info['email'],
            senha=info['senha'],
            celular=info['celular'],
        )
        return JsonResponse({'mensagem': 'Cadastro do usuário efetuado', 'usuario_id': usuario_obj.id}, status=201)
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro ao cadastrar usuário no banco: {str(e)}'}, status=500)

@api_view(['GET'])
def VerificaLogin(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            senha = info['senha']
            if usuario_existe.senha == senha:
                return JsonResponse({"mensagem": "Login efetuado"}) 
            else:
                raise Exception({'mensagem': 'Senha incorreta'})
        else:
            raise Exception({"mensagem": "Email não cadastrado no banco de dados"})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao verificar login","error": str(e)}, status=401)

@api_view(['GET'])
def ExibeInfo(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        nome = usuario_existe.nome
        email = usuario_existe.email
        celular = usuario_existe.celular
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg').first()
        organizacao_nome = organizacao_busca['nomeOrg'] if organizacao_busca else None
        ResponseData = {
            'nome': nome,
            'email': email,
            'celular': celular,
            'organizacao_nome':organizacao_nome,
        }
        return JsonResponse(ResponseData)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar dados de usuario", "error": str(e)}, status=500)    

@api_view(['POST'])
def CriaOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe and (usuario_existe.admGeral == True):
            organizacao_obj = organizacao.objects.create(
                pj_pf=info['pj_pf'],
                cpf_cnpj=info['cpf_cnpj'],
                endContsocial=info['endContsocial'],
                nomeOrg=info['nomeOrg'],
            )
            return JsonResponse({'mensagem': 'Organizacao cadastrada'})
        else:
            raise Exception({'mensagem':'Usuário nao e admin'})
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro ao cadastrar organizacao no banco: {str(e)}'}, status=500)
    
@api_view(['GET'])
def ExibeOrg(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg','cpf_cnpj','idOrganizador','endContsocial','pj_pf').first()
        if organizacao_busca:
            organizacao_nome = organizacao_busca['nomeOrg']
            organizacao_cpf = organizacao_busca['cpf_cnpj']
            organizacao_id = organizacao_busca['idOrganizador']
            organizacao_endereco = organizacao_busca['endContsocial']
            organizacao_razao = organizacao_busca['pj_pf']
            
            ResponseData = {
                'razao_social': organizacao_nome,
                'pj_pf': organizacao_razao,
                'cpf_cnpj':organizacao_cpf,
                'endContsocial': organizacao_endereco,
                'id' : organizacao_id,
                'projetos_associados':'vazio'
            }
            return JsonResponse(ResponseData)
        else:
            ResponseData = {
                'razao_social':'não associado',
                'pj_pf': 'vazio',
                'cpf_cnpj' : 'vazio',
                'endContsocial': 'vazio',
                'id' : 'vazio',
                'projetos_associados':'vazio',
                
            }
            return JsonResponse(ResponseData)
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar dados de organização","error": str(e)}, status=500)

@api_view(['GET'])
def VerificaAdmGeral(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe.admGeral == True:
            return JsonResponse({'mensagem': 'O usuario é um admGeral','usuario':str(usuario_existe.nome)})
        else:
            raise Exception({"mensagem":"Usuario não é AdmGeral", 'usuario':str(usuario_existe.nome)})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao verificar","error": str(e)}, status=500)

@api_view(['POST'])
def ConcedeAdmOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.admOrg = True
            usuario_existe.save()
            return JsonResponse({'mensagem':'Usuario é admin Org' ,'usuario':str(usuario_existe.nome)})
        else:
            raise Exception({'usuario não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario","error": str(e)}, status=500)
    
@api_view(['POST'])
def RemoveAdmOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.admOrg = False
            usuario_existe.save()
            return JsonResponse({'mensagem':'Usuario não é admin Org' ,'usuario':str(usuario_existe.nome)})
        else:
            raise Exception({'usuario não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario","error": str(e)}, status=500)
    
@api_view(['POST'])
def ConcedeAdmInter(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.admInter = True
            usuario_existe.save()
            return JsonResponse({'mensagem':'Usuario é admin Inter' ,'usuario':str(usuario_existe.nome)})
        else:
            raise Exception({'usuario não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario","error": str(e)}, status=500)
    
@api_view(['POST'])
def RemoveAdmInter(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.admInter = False
            usuario_existe.save()
            return JsonResponse({'mensagem':'Usuario não é admin Inter' ,'usuario':str(usuario_existe.nome)})
        else:
            raise Exception({'usuario não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario","error": str(e)}, status=500)