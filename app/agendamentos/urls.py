from django.urls import path
from .views import AgendamentoCreateView

urlpatterns = [
    path('agendamentos/', AgendamentoCreateView.as_view(), name='criar-agendamento'),  # noqa E501

]