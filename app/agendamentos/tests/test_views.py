from datetime import date, timedelta
import pytest
from rest_framework.test import APIClient
from agendamentos.models import Agendamento
from servicos.models import Servico


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def servico():
    return Servico.objects.create(
        nome='Corte de Cabelo',
        duracao_minutos=30,
        preco=50.00,
        ativo=True
    )


@pytest.mark.django_db
def test_cria_agendamento_com_dados_validos(api_client, servico):
    data_futura = date.today() + timedelta(days=1)

    resposta = api_client.post('/api/agendamentos/', {
        'nome_cliente': 'Maria Silva',
        'email_cliente': 'maria@teste.com',
        'telefone_cliente': '11987654321',
        'servico': servico.id,
        'data': data_futura.isoformat(),
        'horario': '14:00',
    })

    assert resposta.status_code == 201
    assert resposta.data['nome_cliente'] == 'Maria Silva'
    assert resposta.data['status'] == 'pendente'


@pytest.mark.django_db
def test_agendamento_criado_e_persistido_no_banco(api_client, servico):
    data_futura = date.today() + timedelta(days=1)

    api_client.post('/api/agendamentos/', {
        'nome_cliente': 'Maria Silva',
        'email_cliente': 'maria@teste.com',
        'telefone_cliente': '11987654321',
        'servico': servico.id,
        'data': data_futura.isoformat(),
        'horario': '14:00',
    })

    assert Agendamento.objects.count() == 1
    assert Agendamento.objects.first().nome_cliente == 'Maria Silva'


@pytest.mark.django_db
def test_rejeita_agendamento_com_data_passada_via_api(api_client, servico):
    data_passada = date.today() - timedelta(days=1)

    resposta = api_client.post('/api/agendamentos/', {
        'nome_cliente': 'Teste Silva',
        'email_cliente': 'teste@teste.com',
        'telefone_cliente': '11999999999',
        'servico': servico.id,
        'data': data_passada.isoformat(),
        'horario': '14:00',
    })

    assert resposta.status_code == 400
    assert 'data' in resposta.data


@pytest.mark.django_db
def test_rejeita_agendamento_duplicado_via_api(api_client, servico):
    data_futura = date.today() + timedelta(days=1)

    Agendamento.objects.create(
        nome_cliente='Primeiro Cliente',
        email_cliente='primeiro@teste.com',
        telefone_cliente='11999999999',
        servico=servico,
        data=data_futura,
        horario='14:00',
    )

    resposta = api_client.post('/api/agendamentos/', {
        'nome_cliente': 'Segundo Cliente',
        'email_cliente': 'segundo@teste.com',
        'telefone_cliente': '11988888888',
        'servico': servico.id,
        'data': data_futura.isoformat(),
        'horario': '14:00',
    })

    assert resposta.status_code == 400


@pytest.mark.django_db
def test_lista_apenas_servicos_ativos(api_client):
    Servico.objects.create(nome='Ativo', duracao_minutos=30, preco=50, ativo=True)  # noqa E501
    Servico.objects.create(nome='Inativo', duracao_minutos=30, preco=50, ativo=False) # noqa E501

    resposta = api_client.get('/api/servicos/')

    assert resposta.status_code == 200
    assert len(resposta.data) == 1
    assert resposta.data[0]['nome'] == 'Ativo'


@pytest.mark.django_db
def test_listagem_de_agendamentos_nao_aceita_get(api_client):
    resposta = api_client.get('/api/agendamentos/')

    assert resposta.status_code == 405