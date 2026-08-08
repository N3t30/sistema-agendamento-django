# Agendix

Sistema de agendamento full-stack com landing page, confirmação automática por email e painel administrativo. Construído como template reutilizável para pequenos negócios (barbearias, clínicas, salões, consultorias) que precisam de um sistema de agendamento simples, sem depender de planilhas ou WhatsApp manual.

## Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Banco de dados**: PostgreSQL 16
- **Frontend**: Django Templates + JavaScript vanilla (sem framework)
- **Email transacional**: SMTP via Brevo
- **Containerização**: Docker + Docker Compose
- **Testes**: pytest + pytest-django

## Por que essa stack

O objetivo do projeto não é demonstrar domínio de tecnologias da moda — é entregar um sistema **funcional, fácil de manter e fácil de adaptar para diferentes clientes**, com o menor número de peças móveis possível.

- **Django Templates em vez de um frontend separado (React/Vue)**: evita duas aplicações, dois deploys, configuração de CORS e build step com Node. Um único container serve tudo — HTML, API e admin.
- **JavaScript vanilla em vez de um framework frontend**: a interatividade necessária (buscar serviços, enviar formulário) é simples o suficiente para não justificar a complexidade extra de um bundler.
- **CSS com variáveis nativas (`:root`)**: permite trocar a identidade visual (cores, marca) de um cliente para outro alterando poucas linhas, sem reescrever a folha de estilos inteira.

## Arquitetura

```
agendix/
├── app/
│   ├── config/              # Configuração central do projeto Django
│   ├── servicos/            # Domínio: cadastro e listagem de serviços
│   ├── agendamentos/        # Domínio: criação e validação de agendamentos
│   ├── templates/           # Landing page (Django Templates)
│   ├── static/              # CSS e JavaScript
│   └── manage.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Cada app Django representa um **domínio de negócio isolado**, não uma divisão técnica arbitrária. Essa separação permite que `servicos` e `agendamentos` evoluam de forma independente — por exemplo, seria possível estender `servicos` para múltiplos profissionais sem tocar na lógica de `agendamentos`.

## Modelagem de dados

### `Servico`
| Campo | Tipo | Observação |
|---|---|---|
| `nome` | CharField | |
| `duracao_minutos` | PositiveIntegerField | Nunca negativo, por design |
| `preco` | DecimalField | **Nunca `FloatField`** — evita erro de arredondamento em valores monetários |
| `ativo` | BooleanField | Soft delete — desativar sem perder histórico de agendamentos vinculados |

### `Agendamento`
| Campo | Tipo | Observação |
|---|---|---|
| `servico` | ForeignKey | `on_delete=PROTECT` — impede apagar um serviço que já tem agendamento vinculado |
| `data`, `horario` | DateField, TimeField | Campos separados para facilitar consultas de disponibilidade |
| `status` | CharField (choices) | `pendente`, `confirmado`, `cancelado` |

**Restrição de integridade**: `unique_together = ('servico', 'data', 'horario')` impede, a nível de banco de dados, dois agendamentos para o mesmo serviço no mesmo horário — inclusive sob condição de corrida (duas requisições simultâneas), o que uma validação apenas em código Python não garantiria sozinha.

## Decisões técnicas relevantes

**Validação em camadas, não apenas uma.** A checagem de horário duplicado existe em três lugares com propósitos diferentes:
1. No frontend (atributo `min` no campo de data) — conveniência de UX, evita erro óbvio antes mesmo de enviar.
2. No serializer (`validate()`) — mensagem de erro amigável e específica.
3. No banco de dados (`unique_together`) — garantia real e definitiva, à prova de condição de corrida.

**Falha de email não compromete o agendamento.** O envio de email usa `fail_silently=True` deliberadamente: se o provedor de email estiver fora do ar, o agendamento já salvo no banco não é perdido nem revertido. O e-mail é tratado como uma notificação complementar, não como parte crítica da transação.

**Variáveis de ambiente centralizadas.** Toda credencial sensível (banco de dados, SMTP) e configuração específica de cliente (`DONO_NEGOCIO_EMAIL`) vive em `.env`, nunca no código. Isso viabiliza reaproveitar o mesmo código-base para múltiplos clientes trocando apenas configuração.

## Rodando o projeto localmente

Pré-requisitos: Docker e Docker Compose instalados.

```bash
git clone https://github.com/seu-usuario/agendix-django-drf.git
cd agendix-django-drf
```

Crie um arquivo `.env` na raiz do projeto:
```env
DB_NAME=agendix
DB_USER=agendix_user
DB_PASSWORD=escolha_uma_senha
DB_HOST=db
DB_PORT=5432
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=seu_login_smtp
EMAIL_HOST_PASSWORD=sua_chave_smtp
EMAIL_USE_TLS=True
```

Suba os containers:
```bash
docker compose up --build
```

Aplique as migrations e crie um superusuário:
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Acesse:
- Landing page: `http://localhost:8000/`
- Painel administrativo: `http://localhost:8000/admin/`
- API de serviços: `http://localhost:8000/api/servicos/`
- API de agendamentos: `http://localhost:8000/api/agendamentos/`

## Rodando os testes

```bash
docker compose exec web pytest agendamentos/tests/ -v
```

A suíte está organizada por camada:
- `test_models.py` — integridade de dados no nível do banco
- `test_serializers.py` — regras de validação isoladas
- `test_views.py` — comportamento fim a fim via API

## Adaptando para um novo cliente

Este projeto foi construído como uma **base reutilizável**, não como um sistema fechado para um único negócio. Para adaptar para um novo cliente, normalmente basta alterar configuração — sem tocar na lógica de negócio.

**O que trocar:**

| O quê | Onde | Exemplo |
|---|---|---|
| Nome do negócio | `templates/base.html` (`<h1 class="logo">`) | "Barbearia do João" |
| Cores da marca | `static/css/style.css` (`:root`) | Trocar `--accent: #6366f1` pela cor do cliente |
| Email de notificação do dono | `.env` (`DONO_NEGOCIO_EMAIL`) | `contato@barbeariadojoao.com` |
| Remetente dos emails | `.env` (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) | Credenciais SMTP próprias do cliente |
| Serviços oferecidos | Django Admin (`/admin/`), após o deploy | Cadastro manual pelo dono do negócio |

**O que normalmente não precisa mudar:** models, serializers, views, validações de negócio (conflito de horário, data passada) — essa é a parte que já é genérica o suficiente para qualquer negócio baseado em agendamento de horário.

**Banco de dados e ambiente**: cada cliente deveria ter sua própria instância do projeto rodando (seu próprio banco de dados, seu próprio deploy) — este não é um sistema multi-tenant (não foi projetado para vários negócios compartilharem a mesma instância/banco).

## Roadmap

- [x] Modelagem de dados com regras de integridade a nível de banco
- [x] API REST (listagem de serviços, criação de agendamentos)
- [x] Validação de disponibilidade de horário
- [x] Envio de email transacional (confirmação + notificação)
- [x] Landing page funcional
- [x] Suíte de testes automatizados
- [ ] Deploy em produção
- [ ] Página de confirmação dedicada
- [ ] Testes de portabilidade entre múltiplos clientes

## Autor

Neto Peixoto — desenvolvedor back-end em formação, focado em Python/Django.