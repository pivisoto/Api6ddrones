from dados.models import organizacao;
from rest_framework import serializers;
class organizacaoSerializer(serializers.ModelSerializer):
        class Meta:
            model = organizacao
            fields = ('idOrganizador','pj_pf','cpf_cnpj','endContsocial','projAssociado','nomeOrg','codOrganizaca','docOrganizacao')