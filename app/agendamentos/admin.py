from django.contrib import admin
from .models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome_cliente', 'servico', 'data', 'horario', 'status')
    list_filter = ('status', 'data')
    search_fields = ('nome_cliente', 'email_cliente')
    ordering = ('data', 'horario')