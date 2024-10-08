from typing import Any
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Usuario(models.Model):
    cnpj = models.CharField(max_length=14)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    localizacao = models.CharField(max_length=200)
    telefone = models.CharField(max_length=30)
    def __str__(self):
        return "{} ({})".format(self.cnpj,self.nome)
    
class Dados(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField()
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.data:
            self.data = datetime.now()
        super().save(*args, **kwargs)

class DadosIntegridade(Dados):
    integridade_placa = models.FloatField()
    eficiencia_placa = models.FloatField()
    def __str__(self):
        return "{} ({})".format(self.usuario.first_name,self.data)
    
class DadosFalha(Dados):
    falha = models.TextField()
    def __str__(self):
        return "{} ({})".format(self.usuario.first_name,self.data)
    
class DadosDesempenho(Dados):
    producao_energetica = models.FloatField()
    consumo_energetico = models.FloatField()
    valor_kwh = models.FloatField()
    lucro = models.FloatField()
    prejuizo = models.FloatField()
    margem = models.FloatField()
    tempo_de_operacao = models.FloatField()
    tempo_de_parada = models.FloatField()
    def __str__(self):
        return "{} ({})".format(self.usuario.first_name,self.data)
    
# cache
class CacheRelatorio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=11)
    data_criacao = models.DateTimeField()
    dados_relatorio = models.JSONField()
    inicio_periodo = models.DateTimeField()
    fim_periodo = models.DateTimeField()
    def __str__(self):
        return "{} ({}) ({})".format(self.usuario.first_name,self.tipo,self.data_criacao)
    def save(self, *args, **kwargs):
        if not self.data_criacao:
            self.data_criacao = datetime.now()
        super().save(*args, **kwargs)
    # class Meta:
    #     abstract = True
    
# class CacheRelatorioConsumo(CacheRelatorio):
#     dados_relatorio = models.TextField()

# class CacheRelatorioFalhas(CacheRelatorio):
#     dados_relatorio = models.TextField()

# class CacheRelatorioIntegridade(CacheRelatorio):
#     dados_relatorio = models.TextField()

# class CacheRelatorioProducao(CacheRelatorio):
#     dados_relatorio = models.TextField()

# class CacheRelatorioProjecao(CacheRelatorio):
#     dados_relatorio = models.TextField()
    
