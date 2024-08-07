from django.db import models

# Create your models here.
class Usuario(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30)
    
class Dados(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
        
class DadosIntegridade(Dados):
    integridade_placa = models.FloatField()
    eficiencia_placa = models.FloatField()
    
class DadosFalhas(Dados):
    falha = models.TextField()
    
class DadosDesempenho(Dados):
    producao_energetica = models.FloatField()
    consumo_energetico = models.FloatField()
    valor_kwh = models.FloatField()
    lucro = models.FloatField()
    prejuizo = models.FloatField()
    margem = models.FloatField()
    tempo_de_operacao = models.FloatField()
    tempo_de_parada = models.FloatField()
    
# cache
class Relatorio(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=11)
    data = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
    
class RelatorioConsumo(Relatorio):
    dados_relatorio = models.TextField()

class RelatorioFalhas(Relatorio):
    dados_relatorio = models.TextField()

class RelatorioIntegridade(Relatorio):
    dados_relatorio = models.TextField()

class RelatorioProducao(Relatorio):
    dados_relatorio = models.TextField()

class RelatorioProjecao(Relatorio):
    dados_relatorio = models.TextField()
    
