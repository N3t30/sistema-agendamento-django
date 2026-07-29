from django.urls import path
from .views import ServicoListView

urlpatterns = [
    path('servicos/', ServicoListView.as_view(), name='lista-servicos'),
]