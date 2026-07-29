from rest_framework import generics
from .models import Servico
from .serializers import ServicoSerializer


class ServicoListView(generics.ListAPIView):
    queryset = Servico.objects.filter(ativo=True)
    serializer_class = ServicoSerializer