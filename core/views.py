from rest_framework import viewsets
from .models import Padaria, Fornada, Inscricao
from .serializers import PadariaSerializer, FornadaSerializer, InscricaoSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class PadariaViewSet(viewsets.ModelViewSet):
    queryset = Padaria.objects.all()
    serializer_class = PadariaSerializer

class FornadaViewSet(viewsets.ModelViewSet):
    queryset = Fornada.objects.all()
    serializer_class = FornadaSerializer

class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Inscricao.objects.filter(usuario=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)