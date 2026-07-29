from rest_framework import serializers
from .models import Servico

class ServicoSerializer(serializers.ModelSerializer): # noqa E302
    class Meta:
        model = Servico
        fields = ['id', 'nome', 'descricao', 'duracao_minutos', 'preco', 'ativo']  # noqa E501
