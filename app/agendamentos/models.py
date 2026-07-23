from django.db import models
from servicos.models import Servico


class Agendamento(models.Model):
    STATUS_CHOICES = [   # Evitar erros de digitaçao para não quebrar em filtros # noqa E501
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]

    nome_cliente = models.CharField(max_length=150)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name='agendamentos') # noqa E501
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente') # noqa E501
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data', 'horario'] # sempre me retornar em ordem de data e hora  # noqa E501
        unique_together = ('servico', 'data', 'horario') # Bloqueio fisico no banco, para não haver dois erviços mesmo horário e data # noqa E501

    def __str__(self):
        return f'{self.nome_cliente} - {self.servico.nome} ({self.data} {self.horario})'  # noqa E501
