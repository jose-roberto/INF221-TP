from django.db import models

# Create your models here.
class usuario(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30)
    
class dados(models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
        
class dados_integridade(dados):
    integridade_placa = models.FloatField()
    eficiencia_placa = models.FloatField()
    
class dados_falhas(dados):
    falha = models.TextField()
    
class dados_desempenho(dados):
    producao_energetica = models.FloatField()
    consumo_energetico = models.FloatField()
    valor_kwh = models.FloatField()
    lucro = models.FloatField()
    prejuizo = models.FloatField()
    margem = models.FloatField()
    tempo_de_operacao = models.FloatField()
    tempo_de_parada = models.FloatField()
    
# cache
class cache_relatorio(models.Model):
    usuario = models.ForeignKey(usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=11)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
class cache_relatorio_consumo(cache_relatorio):
    dados_relatorio = models.TextField()

class cache_relatorio_falhas(cache_relatorio):
    dados_relatorio = models.TextField()

class cache_relatorio_integridade(cache_relatorio):
    dados_relatorio = models.TextField()

class cache_relatorio_producao(cache_relatorio):
    dados_relatorio = models.TextField()

class cache_relatorio_projecao(cache_relatorio):
    dados_relatorio = models.TextField()
    
