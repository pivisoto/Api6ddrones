from django.db import models

class organizacao(models.Model):
    idOrganizador = models.IntegerField(primary_key=True)
    pj_pf = models.CharField(max_length=40)
    cpf_cnpj = models.IntegerField()
    endContsocial = models.CharField(max_length=50)
    docOrganizacao = models.BinaryField()
    nomeOrg = models.CharField(max_length=30)

class projeto(models.Model):
    nomeProjeto = models.CharField(max_length=40)
    descProjeto = models.CharField()
    endProjeto = models.CharField(max_length=50)
    idOrganizador = models.ForeignKey(organizacao,on_delete=models.CASCADE)
    fotosProj = models.BinaryField()
    idProjeto = models.AutoField(primary_key=True)

class usuario(models.Model):
    nome = models.CharField(max_length=40)
    email = models.CharField(max_length=40,unique=True)
    senha = models.CharField(max_length=30)
    imagemPerfil = models.BinaryField(null=True)
    endereco = models.CharField(max_length=50)
    celular = models.CharField()
    idUsuario = models.AutoField(primary_key=True)
    idProjeto = models.ForeignKey(projeto,on_delete=models.CASCADE,null=True)
    idOrganizador = models.ForeignKey(organizacao,on_delete=models.CASCADE,null=True)
    admGeral = models.BooleanField(default=False)
    admOrg = models.BooleanField(default=False)
    admInter = models.BooleanField(default=False)
