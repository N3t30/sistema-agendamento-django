from rest_framework import generics
from .models import Agendamento
from .serializers import AgendamentoSerializer


class AgendamentoCreateView(generics.CreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer 