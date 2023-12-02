from .models import *
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from api.serializers.todos_serializer import todosUsuariosSerializer


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
    
@api_view(['POST'])
def AtualizaUsuario(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.nome = info['nome']
            usuario_existe.celular = info['celular']
            usuario_existe.save()
            return JsonResponse({'mensagem':'Usuario atualizado'})
        else:
            raise Exception({'usuario não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario","error": str(e)}, status=500)
    
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
def CriarOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe and (usuario_existe.admGeral == True):
            organizacao_obj = organizacao.objects.create(
                responsavel = info['responsavel'],
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

@api_view(['POST'])
def DefineIdOrganizador(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe is not None:
            usuario_existe.idOrganizador_id = info['idOrganizador']
            usuario_existe.save()
            return JsonResponse({'mensagem': 'ID do Organizador definido com sucesso'})
        else:
            return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({'mensagem': f'Não foi possível definir o idOrganizador: {str(e)}'}, status=400, safe=False)

@api_view(['POST'])
def AtualizaOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).first()
        if usuario_existe and organizacao_busca:
            organizacao_busca.nomeOrg = info['nomeOrg']
            organizacao_busca.endContsocial = info['endContsocial']
            organizacao_busca.pj_pf = info['pj_pf']
            organizacao_busca.docOrganizacao = info['docOrganizacao']
            organizacao_busca.cpf_cnpj = info['cpf_cnpj']
            organizacao_busca.responsavel = info['responsavel']
            organizacao_busca.save()
            return JsonResponse({'mensagem':'Organizacao atualizado'})
        else:
            raise Exception({'usuario ou organizacao não encontrado'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario ou organizacao","error": str(e)}, status=500)
          
@api_view(['GET'])
def ExibeOrg(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('responsavel','nomeOrg','cpf_cnpj','idOrganizador','endContsocial','pj_pf').first()
        if organizacao_busca:
            organizacao_responsavel = organizacao_busca['responsavel']
            organizacao_cpf = organizacao_busca['cpf_cnpj']
            organizacao_id = organizacao_busca['idOrganizador']
            organizacao_endereco = organizacao_busca['endContsocial']
            organizacao_razao = organizacao_busca['pj_pf']
            organizacao_nome = organizacao_busca['nomeOrg']
            ResponseData = {
                'responsavel': organizacao_responsavel,
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

@api_view(['POST'])
def CriarProjeto(request):
    try:
        info = request.data
        projeto_obj = projeto.objects.create(
        nomeProjeto=info['nomeProjeto'],
        responsavel_projeto=info['responsavel_projeto'],
        descProjeto=info['descProjeto'],
        endProjeto=info['endProjeto'],
        idOrganizador_id=info['idOrganizador']
        )
        return JsonResponse({'mensagem': 'Cadastro do projeto efetuado', 'projeto': info['nomeProjeto']}, status=201)
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro ao cadastrar usuário no banco: {str(e)}'}, status=500)
    
@api_view(['GET'])
def ExibeProjeto(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        projeto_busca = projeto.objects.filter(idProjeto=usuario_existe.idOrganizador_id).values('nomeProjeto','responsavel_projeto','descProjeto','endProjeto').first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg').first()
        if usuario_existe and projeto_busca and organizacao_busca:
            ResponseData = {
                'nomeProjeto': projeto_busca['nomeProjeto'],
                'responsavel_projeto': projeto_busca['responsavel_projeto'],
                'descProjeto': projeto_busca['descProjeto'],
                'endProjeto':projeto_busca['endProjeto'],
                'nomeOrg': organizacao_busca['nomeOrg'],
                'fotos':'vazio'
            }
            return JsonResponse(ResponseData)
        else:
            raise Exception('Não é usuario ou não possui organizacao/projeto')
    except Exception as e:  
        return JsonResponse({'mensagem':f'Não foi possivel exibir os dados do projeto : {str(e)}'})

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
    
@api_view(['GET'])
def VerificaAdmOrg(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe.admOrg == True:
            return JsonResponse({'mensagem': 'O usuario é um admOrg','usuario':str(usuario_existe.nome)})
        else:
            raise Exception({"mensagem":"Usuario não é AdmOrg", 'usuario':str(usuario_existe.nome)})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao verificar","error": str(e)}, status=500)

@api_view(['GET'])
def VerificaAdmInter(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe.admInter == True:
            return JsonResponse({'mensagem': 'O usuario é um admInter','usuario':str(usuario_existe.nome)})
        else:
            raise Exception({"mensagem":"Usuario não é AdmInter", 'usuario':str(usuario_existe.nome)})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao verificar","error": str(e)}, status=500)

@api_view(['POST'])
def ConcedeAdmOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            usuario_existe.admOrg = True
            usuario_existe.admInter = True
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
    
@api_view(['GET'])
def ExibeTodosUsuarios(request):
    all_data = usuario.objects.all()
    serializer = todosUsuariosSerializer(all_data,many=True)
    return JsonResponse(serializer.data,safe=False)