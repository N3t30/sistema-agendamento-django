from django.contrib import admin
from .models import Servico   # Inserindo o models no admin para testar


@admin.register(Servico)  # Decorador  
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'duracao_minutos', 'preco', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome',)