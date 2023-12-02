from api.models import usuario;
from rest_framework import serializers;
class todosUsuariosSerializer(serializers.ModelSerializer):
        class Meta:
            model = usuario
            fields = ('nome','email','senha','celular','idUsuario','admGeral','admOrg','admInter')        