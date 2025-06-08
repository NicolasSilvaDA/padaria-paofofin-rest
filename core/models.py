from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Padaria(models.Model):
    nome = models.CharField(max_length=150)
    endereco = models.TextField()

    def __str__(self):
        return self.nome
    
class Fornada(models.Model):
    padaria = models.ForeignKey(Padaria, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=150)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.padaria.nome} - {self.descricao}'
    
class Inscricao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    padaria = models.ForeignKey(Padaria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'padaria')

    def __str__(self):
        return f'{self.usuario.username} -> {self.padaria.nome}'
