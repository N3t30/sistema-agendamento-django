from datetime import date, timedelta
import pytest
from agendamentos.serializers import AgendamentoSerializer
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


def dados_validos(servico, **sobrescreve):
    base = {
        'nome_cliente': 'Maria Silva',
        'email_cliente': 'maria@teste.com',
        'telefone_cliente': '11987654321',
        'servico': servico.id,
        'data': (date.today() + timedelta(days=1)).isoformat(),
        'horario': '14:00',
    }
    base.update(sobrescreve)
    return base


@pytest.mark.django_db
def test_serializer_valido_com_dados_corretos(servico):
    serializer = AgendamentoSerializer(data=dados_validos(servico))

    assert serializer.is_valid()


@pytest.mark.django_db
def test_serializer_invalido_com_data_passada(servico):
    data_passada = date.today() - timedelta(days=1)
    dados = dados_validos(servico, data=data_passada.isoformat())

    serializer = AgendamentoSerializer(data=dados)

    assert not serializer.is_valid()
    assert 'data' in serializer.errors


@pytest.mark.django_db
def test_serializer_invalido_com_nome_muito_curto(servico):
    dados = dados_validos(servico, nome_cliente='Jo')

    serializer = AgendamentoSerializer(data=dados)

    assert not serializer.is_valid()
    assert 'nome_cliente' in serializer.errors


@pytest.mark.django_db
def test_serializer_invalido_com_telefone_incompleto(servico):
    dados = dados_validos(servico, telefone_cliente='119999')

    serializer = AgendamentoSerializer(data=dados)

    assert not serializer.is_valid()
    assert 'telefone_cliente' in serializer.errors


@pytest.mark.django_db
def test_serializer_invalido_com_horario_duplicado(servico):
    Agendamento.objects.create(
        nome_cliente='Primeiro Cliente',
        email_cliente='primeiro@teste.com',
        telefone_cliente='11999999999',
        servico=servico,
        data=date.today() + timedelta(days=1),
        horario='14:00',
    )

    dados = dados_validos(servico, horario='14:00')
    serializer = AgendamentoSerializer(data=dados)

    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors