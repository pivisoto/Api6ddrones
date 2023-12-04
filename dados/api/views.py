from .models import *
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from api.serializers import todosUsuariosSerializer,organizacaoSerializer,proojetoSerializer
from django.core.mail import send_mail
from random import randrange
import re

@api_view(['POST'])
def VerificaUsuarioExiste(request):
    try:
        info = request.data
        email_cadastrado = usuario.objects.filter(email=info['email']).first()
        if email_cadastrado:
            return JsonResponse({'mensagem': 'Este email já está cadastrado'}, status=200)
        else:
            CadastraUsuario(request)
            return JsonResponse({'mensagem': 'Usuário cadastrado'})
    except Exception as e:
        return JsonResponse({'mensagem': f'Erro na verificação de existência do email: {str(e)}'}, status=500)

def CadastraUsuario(request):
    try:
        info = request.data
        senha_teste = info['senha']
        if (len(senha_teste) >= 8 and any(char.isdigit() for char in senha_teste) and any(char.isupper() for char in senha_teste) and re.search(r'[!@#$%^&*(),.?":{}|<>]', senha_teste)):
            usuario_obj = usuario.objects.create(
                nome=info['nome'],
                email=info['email'],
                senha=info['senha'],
                celular=info['celular'],
            )
            return JsonResponse({'mensagem': 'Cadastro do usuário efetuado', 'usuario_id': usuario_obj.id}, status=201)
        else:
            raise Exception('Senha não corresponde aos requisitos')   
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
        if usuario_existe and (usuario_existe.admOrg == True):
            organizacao_obj = organizacao.objects.create(
                responsavel = info['responsavel'],
                pj_pf=info['pj_pf'],
                cpf_cnpj=info['cpf_cnpj'],
                endContsocial=info['endContsocial'],
                nomeOrg=info['nomeOrg'],
                docOrganizacao=info['docOrganizacao']
            )
            usuario_existe.idOrganizador_id = organizacao_obj.idOrganizador
            usuario_existe.save()
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
        usuario_adicao = usuario.objects.filter(email=info['emailAdicao']).first()
        if usuario_existe is not None and usuario_adicao is not None and usuario_existe.admOrg == True:
            usuario_adicao.idOrganizador_id = info['idOrganizador']
            usuario_adicao.save()
            return JsonResponse({'mensagem': 'ID do Organizador definido com sucesso'})
        else:
            return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({'mensagem': f'Não foi possível definir o idOrganizador: {str(e)}'}, status=400, safe=False)
    
@api_view(['POST'])
def RemovePessoaOrganizacao(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador = usuario_existe.idOrganizador_id).first()
        if usuario_existe and organizacao_busca and usuario_existe.admOrg == True:
            usuario_existe.idOrganizador_id = None
            usuario_existe.idProjeto_id = None
            usuario_existe.admOrg = False
            usuario_existe.admInter = False
            usuario_existe.save()
            return JsonResponse({'mensagem': 'Usuario removido da organização'})
        else:
            return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({'mensagem': f'Não foi possivel remover o usuario: {str(e)}'}, status=400, safe=False)
    
@api_view(['POST'])
def AtualizaOrg(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).first()
        if usuario_existe and organizacao_busca and usuario_existe.admOrg == True:
            organizacao_busca.nomeOrg = info['nomeOrg']
            organizacao_busca.endContsocial = info['endContsocial']
            organizacao_busca.pj_pf = info['pj_pf']
            organizacao_busca.docOrganizacao = info['docOrganizacao']
            organizacao_busca.cpf_cnpj = info['cpf_cnpj']
            organizacao_busca.responsavel = info['responsavel']
            organizacao_busca.save()
            return JsonResponse({'mensagem':'Organizacao atualizado'})
        else:
            raise Exception({'usuario ou organizacao não encontrado , usuario não tem permissão'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario ou organizacao","error": str(e)}, status=500)
          
@api_view(['GET'])
def ExibeOrg(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).first()
        if organizacao_busca:
            organizacao_responsavel = organizacao_busca.responsavel
            organizacao_cpf = organizacao_busca.cpf_cnpj
            organizacao_id = organizacao_busca.idOrganizador
            organizacao_endereco = organizacao_busca.endContsocial
            organizacao_razao = organizacao_busca.pj_pf
            organizacao_nome = organizacao_busca.nomeOrg
            organizacao_doc = organizacao_busca.docOrganizacao
            projetos_associados = projeto.objects.filter(idOrganizador=organizacao_busca).values_list('nomeProjeto', flat=True)
            ResponseData = {
                'responsavel': organizacao_responsavel,
                'nomeOrg': organizacao_nome,
                'pj_pf': organizacao_razao,
                'cpf_cnpj': organizacao_cpf,
                'endContsocial': organizacao_endereco,
                'id': organizacao_id,
                'docOrganizacao': organizacao_doc,
                'projetos_associados': list(projetos_associados)
            }
            return JsonResponse(ResponseData)
        else:
            return JsonResponse({'Não possui organizacao'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar dados de organização", "error": str(e)}, status=500)

@api_view(['POST'])
def CriarProjeto(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe and usuario_existe.admInter == True:
            organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).first()
            if organizacao_busca:
                projeto_obj = projeto.objects.create(
                    nomeProjeto=info['nomeProjeto'],
                    responsavel_projeto=info['responsavel_projeto'],
                    descProjeto=info['descProjeto'],
                    fotosProj=info['fotosProj'],
                    endProjeto=info['endProjeto'],
                    idOrganizador=organizacao_busca
                )
                usuario_existe.idProjeto = projeto_obj
                usuario_existe.save()
                organizacao_busca.idProjeto = projeto_obj
                organizacao_busca.save()
                return JsonResponse({'mensagem': 'Cadastro do projeto efetuado', 'projeto': info['nomeProjeto']}, status=201)
            else:
                raise Exception('Organização não encontrada')
        else:
            raise Exception('Usuário não autorizado ou informações inválidas')

    except Exception as e:
        return JsonResponse({'mensagem': f'Erro ao cadastrar usuário no banco: {str(e)}'}, status=500)
    
@api_view(['POST'])
def AtualizaProjeto(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        projeto_busca = projeto.objects.filter(idProjeto=info['idProjeto']).first()
        usuario_pertence = usuario.objects.filter(idProjeto=projeto_busca.idProjeto).first()
        if usuario_existe and projeto_busca and usuario_existe.admInter == True:
            projeto_busca.nomeProjeto = info['nomeProjeto']
            projeto_busca.descProjeto = info['descProjeto']
            projeto_busca.endProjeto = info['endProjeto']
            projeto_busca.fotosProj = info['fotosProj']
            projeto_busca.responsavel_projeto= info['responsavel_projeto']
            projeto_busca.save()
            return JsonResponse({'mensagem':'Organizacao atualizado'})
        else:
            raise Exception({'usuario ou organizacao não encontrado , usuario não tem permissão'})
    except Exception as e:
        return JsonResponse({"mensagem": "Erro ao encontrar usuario ou organizacao","error": str(e)}, status=500)   
    
@api_view(['GET'])
def ExibeProjeto(request):
    try:
        info = request.query_params
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        projeto_busca = projeto.objects.filter(idProjeto=usuario_existe.idProjeto_id).values('nomeProjeto','responsavel_projeto','descProjeto','endProjeto','fotosProj','idProjeto').first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).values('nomeOrg').first()
        if usuario_existe and projeto_busca and organizacao_busca:
            ResponseData = {
                'nomeProjeto': projeto_busca['nomeProjeto'],
                'responsavel_projeto': projeto_busca['responsavel_projeto'],
                'descProjeto': projeto_busca['descProjeto'],
                'endProjeto':projeto_busca['endProjeto'],
                'nomeOrg': organizacao_busca['nomeOrg'],
                'fotos':projeto_busca['fotosProj'],
                'idProjeto':projeto_busca['idProjeto']
            }
            return JsonResponse(ResponseData)
        else:
            raise Exception('Não é usuario ou não possui organizacao/projeto')
    except Exception as e:  
        return JsonResponse({'mensagem':f'Não foi possivel exibir os dados do projeto : {str(e)}'})
    
@api_view(['POST'])
def DefineIdProjeto(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        usuario_adicao = usuario.objects.filter(email=info['emailAdicao']).first()
        if usuario_existe is not None and usuario_adicao is not None and usuario_existe.admInter == True:
            usuario_adicao.idProjeto_id = info['idProjeto']
            usuario_adicao.save()
            return JsonResponse({'mensagem': 'Id do Projeto definido com sucesso'})
        else:
            return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({'mensagem': f'Não foi possível definir o idProjeto: {str(e)}'}, status=400, safe=False)

@api_view(['POST'])
def RemovePessoaProjeto(request):
    try:
        info = request.data
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        projeto_busca = projeto.objects.filter(idProjeto = usuario_existe.idProjeto_id).first()
        if usuario_existe and projeto_busca and usuario_existe.admInter == True:
            usuario_existe.idProjeto_id = None
            usuario_existe.save()
            return JsonResponse({'mensagem': 'Usuario removido do Projeto'})
        else:
            return JsonResponse({'mensagem': 'Usuário não encontrado'}, status=400, safe=False)
    except Exception as e:
        return JsonResponse({'mensagem': f'Não foi possivel remover o usuario: {str(e)}'}, status=400, safe=False)

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
#testado    
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
#testado
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
#testado
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
#testado   
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
#testado    
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
#testado       
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

#testado
def MandaEmail(email,codigo):
    send_mail(
    "Código de verificação",
    f"Este é o código para trocar sua senha {codigo}",
    "from@example.com",
    [email],
    fail_silently=False,
)
#testado    
@api_view(['GET'])
def RecebeEmail(request):
    try:
        info = request.query_params
        codigo = randrange(10000,99999)
        email = info['email']
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe:
            MandaEmail(email,codigo)
            ResponseData = {
                'codigo_usuario' : codigo
            }
            return JsonResponse(ResponseData)
        else:
            raise Exception('Email não cadastrado')
    except Exception as e:
        return JsonResponse(f'Nao foi possivel enviar o email , {str(e)}',safe=False)
#testado       
@api_view(['POST'])
def AtualizaSenha(request):
    try:
        info = request.data
        senha = info['senha']
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        if usuario_existe and (len(senha) >= 8 and any(char.isdigit() for char in senha) and any(char.isupper() for char in senha) and re.search(r'[!@#$%^&*(),.?":{}|<>]', senha)):
            usuario_existe.senha = senha
            usuario_existe.save()
            return JsonResponse({'mensagem': 'Senha atualizada'}, safe=False)
        else:
            raise Exception('Usuário não existe ou a senha não corresponde ao requisitos')
    except Exception as e:
        return JsonResponse({'mensagem': f"Não foi possível mudar a senha. Erro: {e}"}, safe=False)
#testado    
@api_view(['GET'])
def ExibeTodosUsuarios(request):
    all_data = usuario.objects.all()
    serializer = todosUsuariosSerializer(all_data,many=True)
    return JsonResponse(serializer.data,safe=False)
    
@api_view(['GET'])
def ExibeTodasOrganizacoes(request):
    all_data = organizacao.objects.all()
    serializer = organizacaoSerializer(all_data,many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def ExibeTodosProjetos(request):
    all_data = projeto.objects.all()
    serializer = proojetoSerializer(all_data,many=True)
    return JsonResponse(serializer.data,safe=False)

@api_view(['POST'])
def ApagaOrg(request):
    try:
        info = request.data
        idOrg = info['idOrganizador']
        print(idOrg)
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        organizacao_busca = organizacao.objects.filter(idOrganizador=usuario_existe.idOrganizador_id).first()
        if usuario_existe and idOrg == organizacao_busca.idOrganizador and usuario_existe.admOrg == True:
            usuarios_associados_org = usuario.objects.filter(idOrganizador_id=idOrg).first()
            if usuarios_associados_org:
                usuarios_associados_org.idOrganizador_id = None
                usuarios_associados_org.save()
            projeto_busca = projeto.objects.filter(idProjeto=organizacao_busca.idProjeto_id).first()
            if projeto_busca:
                usuarios_associados_proj = usuario.objects.filter(idProjeto_id=projeto_busca.idProjeto).first()
                if usuarios_associados_proj:
                    usuarios_associados_proj.idProjeto_id = None
                    usuarios_associados_proj.save()
                projeto_busca.delete()
            organizacao_busca.delete()
            return JsonResponse({'mensagem': 'Organização e seus projetos foram deletados'}, safe=False)
        else:
            raise Exception('Usuário ou organização não encontrado, ou usuário não tem permissão')
    except Exception as e:
        return JsonResponse({'mensagem': f"Não foi possível deletar a organização. Erro: {e}"}, safe=False)

@api_view(['POST'])
def ApagaProjeto(request):
    try:
        info = request.data
        idProj = info['idProjeto']
        usuario_existe = usuario.objects.filter(email=info['email']).first()
        projeto_busca = projeto.objects.filter(idProjeto=usuario_existe.idProjeto_id).first()
        if usuario_existe and idProj == projeto_busca.idProjeto and usuario_existe.admInter == True:
            usuarios_associados_proj = usuario.objects.filter(idProjeto_id=idProj).first()
            if usuarios_associados_proj:
                usuarios_associados_proj.idProjeto_id = None
                usuarios_associados_proj.save()
            organizacao_busca = organizacao.objects.filter(idProjeto_id=projeto_busca.idProjeto).first()
            if organizacao_busca:
                organizacao_busca.idProjeto_id = None
                organizacao_busca.save()
                projeto_busca.delete()
            return JsonResponse({'mensagem': 'Projeto foi deletado'}, safe=False)
        else:
            raise Exception('Usuário ou projeto não encontrado, ou usuário não tem permissão')
    except Exception as e:
        return JsonResponse({'mensagem': f"Não foi possível deletar o projeto. Erro: {e}"}, safe=False)