from rest_framework import serializers
from .models import Padaria, Produto, Fornada, Inscricao

class PadariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padaria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class FornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornada
        fields = '__all__'

class InscricaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscricao
        fields = '__all__'
