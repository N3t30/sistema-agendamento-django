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
        validators = []  # Preciso que o meu validate funcione, isso zera os validatores automaticos # noqa E501

    def validate(self, dados):
        servico = dados.get('servico')
        data = dados.get('data')
        horario = dados.get('horario')

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