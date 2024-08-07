from django.db import models

# Create your models here.
class Usina(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30)
    
class DadosIntegridade(models.Model):
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    integridade_placa = models.FloatField()
    eficiencia_placa = models.FloatField()
    
class DadosFalhas(models.Model):
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    falha = models.TextField()
    
class DadosDesempenho(models.Model):
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    producao_energetica = models.FloatField()
    consumo_energetico = models.FloatField()
    valor_kwh = models.FloatField()
    lucro = models.FloatField()
    prejuizo = models.FloatField()
    margem = models.FloatField()
    tempo_de_operacao = models.FloatField()
    tempo_de_parada = models.FloatField()
    
class Relatorio(models.Model):
    usina = models.ForeignKey(Usina, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=11)
    dados_relatorio = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    
