from datetime import date
from django.utils import timezone
from rest_framework import serializers
from .models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            'id', 'nome_cliente', 'email_cliente', 'telefone_cliente',
            'servico', 'data', 'horario', 'status', 'criado_em'
        ]
        read_only_fields = ['status', 'criado_em']
        validators = []

    def validate_data(self, valor):
        if valor < date.today():
            raise serializers.ValidationError('A data não pode estar no passado.') # noqa E501
        return valor

    def validate_nome_cliente(self, valor):
        if len(valor.strip()) < 3:
            raise serializers.ValidationError('O nome deve ter pelo menos 3 caracteres.')  # noqa E501
        return valor

    def validate_telefone_cliente(self, valor):
        numeros = ''.join(filter(str.isdigit, valor))
        if len(numeros) < 10 or len(numeros) > 11:
            raise serializers.ValidationError('Telefone inválido. Use DDD + número (10 ou 11 dígitos).')  # noqa E501  
        return valor

    def validate(self, dados):
        servico = dados.get('servico')
        data = dados.get('data')
        horario = dados.get('horario')

        if data == date.today():
            agora = timezone.localtime().time()
            if horario < agora:
                raise serializers.ValidationError(
                    'O horário selecionado já passou para o dia de hoje.'  # noqa E501
                )

        conflito = Agendamento.objects.filter(
            servico=servico,
            data=data,
            horario=horario
        ).exists()

        if conflito:
            raise serializers.ValidationError(
                'Esse horário já está ocupado para o serviço selecionado. Escolha outro horário.'  # noqa E501
            )

        return dados