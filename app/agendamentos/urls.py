from django.urls import path
from .views import AgendamentoCreateView
from .views import landing_page

urlpatterns = [
    path('', landing_page, name='landing-page'),
    path('agendamentos/', AgendamentoCreateView.as_view(), name='criar-agendamento'),  # noqa E501

]