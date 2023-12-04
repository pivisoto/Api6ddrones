from api.models import usuario;
from api.models import organizacao;
from rest_framework import serializers;
from rest_framework import serializers

class todosUsuariosSerializer(serializers.ModelSerializer):
    nomeOrg = serializers.SerializerMethodField()

    class Meta:
        model = usuario
        fields = ('nome', 'email', 'celular', 'idUsuario', 'admGeral', 'admOrg', 'admInter', 'nomeOrg')

    def get_nomeOrg(self, obj):
            id_organizacao = obj.idOrganizador_id   
            if id_organizacao is not None:         
                organizacao_busca = organizacao.objects.filter(idOrganizador=id_organizacao).values('nomeOrg').first()
                if organizacao_busca:
                    nome_org = organizacao_busca['nomeOrg']
                    return nome_org
            return None