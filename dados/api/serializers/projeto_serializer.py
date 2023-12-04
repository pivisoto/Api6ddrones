from api.models import projeto , organizacao;
from rest_framework import serializers;
class proojetoSerializer(serializers.ModelSerializer):
    nomeOrg = serializers.SerializerMethodField()
    class Meta:
        model = projeto
        fields = ('nomeProjeto','descProjeto','endProjeto','idOrganizador','fotosProj','idProjeto','responsavel_projeto','nomeOrg')        
            
    def get_nomeOrg(self, obj):
        id_organizacao = obj.idOrganizador_id   
        if id_organizacao is not None:         
            organizacao_busca = organizacao.objects.filter(idOrganizador=id_organizacao).values('nomeOrg').first()
            if organizacao_busca:
                nome_org = organizacao_busca['nomeOrg']
                return nome_org
            return None