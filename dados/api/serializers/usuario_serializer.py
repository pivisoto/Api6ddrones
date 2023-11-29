from api.models import *
from rest_framework import serializers;
import re

class usuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    #necessariamente esse nome validate_nome_do_campo
    def validate_password(self,senha):
        if not re.search('[0-9]',senha):
            raise serializers.ValidationError("A senha deve conter pelo menos um número")
        if not re.search('[^a-zA-Z0-9]', senha):
            raise serializers.ValidationError("A senha deve conter pelo menos um caracter especial")
        if len(senha) < 8:
            raise serializers.ValidationError("A senha deve conter pelo menos oito caracteres")
        return senha

    class Meta:
        model = usuario
        fields = ('nome','email','senha','imagemPerfil','endereco','celular','idUsuario','idProjeto','idOrganizador','admGeral','admOrg','admInter')
