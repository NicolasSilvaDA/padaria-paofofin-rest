from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Perfil(models.Model):
    TIPO_USUARIO = (
        ('pessoa', 'Pessoa'),
        ('padaria', 'Padaria'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO)
    nome_padaria = models.CharField(max_length=150, blank=True, null=True) # Apenas para Padaria

    def __str__(self) -> str:
        return f'{self.usuario.username} ({self.tipo})'

class Padaria(models.Model):
    nome = models.CharField(max_length=150)
    endereco = models.TextField()

    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=80)
    descricao = models.TextField(blank=True)
    padaria = models.ForeignKey(User, related_name='produtos', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.nome} ({self.padaria.username})'

    
class Fornada(models.Model):
    padaria = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, null=True) # remover null após resolver cadastro de produtos
    descricao = models.CharField(max_length=150, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Fornada de {self.produto.nome} em {self.padaria.username} às {self.data_criacao}' # type: ignore
    
class Inscricao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    padaria = models.ForeignKey(Padaria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'padaria')

    def __str__(self):
        return f'{self.usuario.username} -> {self.padaria.nome}'
