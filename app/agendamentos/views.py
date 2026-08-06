from rest_framework import generics
from .models import Agendamento
from .serializers import AgendamentoSerializer
from django.core.mail import send_mail
from django.conf import settings


class AgendamentoCreateView(generics.CreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer 

    def perform_create(self, serializer):
        agendamento = serializer.save()
        self.enviar_email_confirmacao(agendamento)
        self.enviar_email_notificacao_dono(agendamento)

    def enviar_email_confirmacao(self, agendamento):
        send_mail(
            subject='Confirmação de Agendamento', 
            message=(
                f'Olá {agendamento.nome_cliente},\n\n'
                f'Seu agendamento para {agendamento.servico.nome} foi confirmado '# noqa E501
                f'para o dia {agendamento.data} às {agendamento.horario}.\n\n'
                f'Obrigado por agendar conosco!'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[agendamento.email_cliente],
            fail_silently=True # Apenas para controlar a falha no envio do e-mail   # noqa E501
        )
    
    def enviar_email_notificacao_dono(self, agendamento):
        send_mail(
            subject='Novo Agendamento Recebido', 
            message=(
                f'Novo agendamento de {agendamento.nome_cliente} para o serviço {agendamento.servico.nome}'  # noqa E501
                f' No dia {agendamento.data} às {agendamento.horario}.'         
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DONO_NEGOCIO_EMAIL],
            fail_silently=True # Apenas para controlar a falha no envio do e-mail # noqa E501
        )
