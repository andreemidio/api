from rest_framework import serializers
from .models import Documentos, LogConsulta


class DocumentosSerializer(serializers.ModelSerializer):
    class Meta:
        modeL = Documentos
        fields = '__all__'


class LogConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogConsulta
        fields = '__all__'
