from .models import Padaria, Fornada, Inscricao
from .serializers import PadariaSerializer, FornadaSerializer, InscricaoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# Class-Based Views (API)

class PadariaViewSet(viewsets.ModelViewSet):
    queryset = Padaria.objects.all()
    serializer_class = PadariaSerializer
    permission_classes = [IsAuthenticated]

class FornadaViewSet(viewsets.ModelViewSet):
    queryset = Fornada.objects.all()
    serializer_class = FornadaSerializer
    permission_classes = [IsAuthenticated]

class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        user = self.request.user
        return Inscricao.objects.filter(usuario=user)
    
    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

# HTML views

@login_required
def index(request):
    padarias = Padaria.objects.all()
    inscricoes = Inscricao.objects.filter(usuario=request.user).values_list('padaria_id', flat=True)
    return render(
        request,
        'core/index.html',
        {
            'padarias' : padarias,
            'inscricoes' : inscricoes,
        }
    )

# Gather Data / Redirect Views

def sair(request):
    logout(request)
    return redirect('login')

@login_required
def inscrever_usuario_padaria(request, padaria_id):
    padaria = get_object_or_404(Padaria, pk=padaria_id)
    Inscricao.objects.get_or_create(usuario=request.user, padaria=padaria)
    return redirect('index')

@login_required
def desinscrever_usuario_padaria(request, padaria_id):
    # padaria = get_object_or_404(Padaria, pk=padaria_id)
    inscricao_usuario = Inscricao.objects.filter(padaria_id=padaria_id, usuario=request.user)
    if inscricao_usuario.exists():
        inscricao_usuario.delete()

    return redirect('index')