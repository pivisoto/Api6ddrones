from api.models import projeto;
from rest_framework import serializers;
class proojetoSerializer(serializers.ModelSerializer):
        class Meta:
            model = projeto
            fields = ('nomeProjeto','descProjeto','endProjeto','idOrganizador','fotosProj','idProjeto')        