from datetime import date, timedelta
import pytest
from django.db import IntegrityError
from agendamentos.models import Agendamento
from servicos.models import Servico


@pytest.fixture
def servico():
    return Servico.objects.create(
        nome='Corte de Cabelo',
        duracao_minutos=30,
        preco=50.00,
        ativo=True
    )


@pytest.mark.django_db
def test_nao_permite_dois_agendamentos_com_mesmo_servico_data_horario(servico):
    data_futura = date.today() + timedelta(days=1)

    Agendamento.objects.create(
        nome_cliente='Primeiro Cliente',
        email_cliente='primeiro@teste.com',
        telefone_cliente='11999999999',
        servico=servico,
        data=data_futura,
        horario='14:00',
    )

    with pytest.raises(IntegrityError):
        Agendamento.objects.create(
            nome_cliente='Segundo Cliente',
            email_cliente='segundo@teste.com',
            telefone_cliente='11988888888',
            servico=servico,
            data=data_futura,
            horario='14:00',
        )


@pytest.mark.django_db
def test_str_do_agendamento_mostra_informacoes_relevantes(servico):
    agendamento = Agendamento.objects.create(
        nome_cliente='Maria Silva',
        email_cliente='maria@teste.com',
        telefone_cliente='11999999999',
        servico=servico,
        data=date.today() + timedelta(days=1),
        horario='14:00',
    )

    assert 'Maria Silva' in str(agendamento)
    assert 'Corte de Cabelo' in str(agendamento)


@pytest.mark.django_db
def test_nao_permite_deletar_servico_com_agendamento_vinculado(servico):
    Agendamento.objects.create(
        nome_cliente='Cliente Teste',
        email_cliente='teste@teste.com',
        telefone_cliente='11999999999',
        servico=servico,
        data=date.today() + timedelta(days=1),
        horario='14:00',
    )

    with pytest.raises(Exception):
        servico.delete()