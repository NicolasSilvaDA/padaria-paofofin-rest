from .models import Padaria, Produto, Fornada, Inscricao, Perfil
from .serializers import PadariaSerializer, ProdutoSerializer, FornadaSerializer, InscricaoSerializer
from .forms import UsuarioCadastroForm
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.

# Class-Based Views (API)

class PadariaViewSet(viewsets.ModelViewSet):
    queryset = Padaria.objects.all()
    serializer_class = PadariaSerializer
    permission_classes = [IsAuthenticated]

class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        return Produto.objects.filter(padaria=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(padaria=self.request.user)

class FornadaViewSet(viewsets.ModelViewSet):
    queryset = Fornada.objects.all() # Deletar quando configurar
    serializer_class = FornadaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # type: ignore
        return Fornada.objects.filter(padaria=self.request.user)
    
    def perform_create(self, serializer):
        fornada = serializer.save(padaria=self.request.user)
        # notificar_inscritos(fornada)

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

def index(request):
    if hasattr(request.user, 'perfil'):
        perfil = getattr(request.user.perfil, 'tipo')
        inscricoes = Inscricao.objects.filter(usuario=request.user).values_list('padaria_id', flat=True)

        if perfil == 'pessoa':
            padarias = Padaria.objects.all()
            return render(
                request,
                'core/home_usuario.html',
                {
                    'padarias' : padarias,
                    'inscricoes' : inscricoes,
                }
            )
        
        produtos = Produto.objects.filter(padaria_id=request.user)
        return render(
            request,
            'core/home_padaria.html',
            {
                'produtos': produtos,
                'inscricoes' : inscricoes
            }
        )

    padarias = Padaria.objects.all()
    return render(
        request,
        'core/index.html',
        {
            'padarias' : padarias,
        }
    )


@login_required # VER DEPOIS
def criar_fornada(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'padaria':
        messages.error(request, "Apenas padarias podem criar fornadas.")
        return redirect('index')
    
    produtos = Produto.objects.filter(padaria=request.user)

    if not produtos.exists():
        messages.warning(request, "Você precisa registrar pelo menos um produto antes de criar uma fornada!")
        return redirect('cadastrar_produto')

    if request.method == 'POST':
        produto_id = request.POST.get('produto')
        produto = get_object_or_404(Produto, id=produto_id, padaria=request.user)

        Fornada.objects.create(produto=produto, padaria=request.user)

        # Aviso de sucesso para o usuário fazendo a fornada
        messages.success(request, f'Fornada de {produto.nome} criada com sucesso! Todos os usuário inscritos foram notificados!')

        return redirect('padarias')
    else:
        produtos = Produto.objects.filter(padaria=request.user)
        return render(
            request,
            'core/criar_fornada,html',
            {'produtos' : produtos}
        )

# Gather Data / Redirect Views

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            tipo = form.cleaned_data['tipo']
            Perfil.objects.create(usuario=user, tipo=tipo)
            messages.success(request, 'Conta criada com sucesso.') # VER DEPOIS
            return redirect('login')
    else:
        form = UsuarioCadastroForm()
        
    return render(
        request,
        'cadastro.html',
        {'form': form},
    )

def sair(request):
    logout(request)
    return redirect('index')

@login_required
def inscrever_usuario_padaria(request, padaria_id):
    padaria = get_object_or_404(Padaria, pk=padaria_id)
    Inscricao.objects.get_or_create(usuario=request.user, padaria=padaria)
    return redirect('home_usuario')

@login_required
def desinscrever_usuario_padaria(request, padaria_id):
    # padaria = get_object_or_404(Padaria, pk=padaria_id)
    inscricao_usuario = Inscricao.objects.filter(padaria_id=padaria_id, usuario=request.user)
    if inscricao_usuario.exists():
        inscricao_usuario.delete()

    return redirect('home_usuario')
