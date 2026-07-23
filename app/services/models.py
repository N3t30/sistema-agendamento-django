from django.db import models


class Services(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    duracao_minutos = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    ativo = models.BooleanField(default=True)  # Aqui seria um soft delete caso seja nescessário excluir algum servico.  # noqa E501
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome