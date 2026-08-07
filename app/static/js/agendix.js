function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrftoken = getCookie('csrftoken');

async function carregarServicos() {
    const container = document.getElementById('lista-servicos');
    const select = document.getElementById('servico');

    try {
        const response = await fetch('/api/servicos/');
        const servicos = await response.json();

        if (servicos.length === 0) {
            container.innerHTML = '<p class="carregando">Nenhum serviço disponível no momento.</p>';
            return;
        }

        container.innerHTML = '';
        servicos.forEach(servico => {
            const card = document.createElement('div');
            card.className = 'servico-card';
            card.innerHTML = `
                <div>
                    <div class="servico-nome">${servico.nome}</div>
                    <div class="servico-detalhes">${servico.duracao_minutos} min</div>
                </div>
                <div class="servico-preco">R$ ${parseFloat(servico.preco).toFixed(2)}</div>
            `;
            container.appendChild(card);

            const option = document.createElement('option');
            option.value = servico.id;
            option.textContent = servico.nome;
            select.appendChild(option);
        });
    } catch (erro) {
        container.innerHTML = '<p class="carregando">Erro ao carregar serviços. Tente recarregar a página.</p>';
    }
}

async function enviarAgendamento(evento) {
    evento.preventDefault();

    const mensagem = document.getElementById('mensagem');
    const botao = document.querySelector('.botao-enviar');
    const form = document.getElementById('form-agendamento');

    const dados = {
        nome_cliente: document.getElementById('nome_cliente').value,
        email_cliente: document.getElementById('email_cliente').value,
        telefone_cliente: document.getElementById('telefone_cliente').value,
        servico: document.getElementById('servico').value,
        data: document.getElementById('data').value,
        horario: document.getElementById('horario').value,
    };

    botao.disabled = true;
    botao.textContent = 'Enviando...';
    mensagem.className = 'mensagem';

    try {
        const response = await fetch('/api/agendamentos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(dados),
        });

        if (response.ok) {
            mensagem.textContent = 'Agendamento confirmado! Você receberá um email de confirmação em instantes.';
            mensagem.className = 'mensagem sucesso';
            form.reset();
        } else {
            const erro = await response.json();
            const primeiraChave = Object.keys(erro)[0];
            const primeiraMensagem = Array.isArray(erro[primeiraChave]) ? erro[primeiraChave][0] : erro[primeiraChave];
            mensagem.textContent = primeiraMensagem || 'Não foi possível concluir o agendamento. Verifique os dados e tente novamente.';
            mensagem.className = 'mensagem erro';
        }
    } catch (erro) {
        mensagem.textContent = 'Erro de conexão. Tente novamente.';
        mensagem.className = 'mensagem erro';
    } finally {
        botao.disabled = false;
        botao.textContent = 'Confirmar agendamento';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const hoje = new Date().toISOString().split('T')[0];
    document.getElementById('data').setAttribute('min', hoje);

    carregarServicos();
    document.getElementById('form-agendamento').addEventListener('submit', enviarAgendamento);
});