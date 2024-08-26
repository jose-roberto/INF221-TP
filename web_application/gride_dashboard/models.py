from django.db import models
from django.contrib.auth.models import User

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
    data = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True

class DadosIntegridade(Dados):
    integridade_placa = models.FloatField()
    eficiencia_placa = models.FloatField()
    def __init__(self, usuario, integridade_placa, eficiencia_placa):
        self.usuario = usuario
        self.integridade_placa = integridade_placa
        self.eficiencia_placa = eficiencia_placa
    def __str__(self):
        return "{} ({})".format(self.usuario.first_name,self.data)
    
class DadosFalha(Dados):
    falha = models.TextField()
    def __init__(self, usuario, falha):
        self.usuario = usuario
        self.falha = falha
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
    def __init__(self, usuario, producao_energetica, consumo_energetico, valor_kwh, lucro, prejuizo, margem, tempo_de_operacao, tempo_de_parada):
        self.usuario = usuario
        self.producao_energetica = producao_energetica
        self.consumo_energetico = consumo_energetico
        self.valor_kwh = valor_kwh
        self.lucro = lucro
        self.prejuizo = prejuizo
        self.margem = margem
        self.tempo_de_operacao = tempo_de_operacao
        self.tempo_de_parada = tempo_de_parada
    def __str__(self):
        return "{} ({})".format(self.usuario.first_name,self.data)
    
# cache
class CacheRelatorio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=11)
    data_criacao = models.DateTimeField(auto_now_add=True)
    dados_relatorio = models.JSONField()
    inicio_periodo = models.DateTimeField()
    fim_periodo = models.DateTimeField()
    def __init__(self, usuario, tipo, dados_relatorio, inicio_periodo, fim_periodo):
        self.usuario = usuario
        self.tipo = tipo
        self.dados_relatorio = dados_relatorio
        self.inicio_periodo = inicio_periodo
        self.fim_periodo = fim_periodo
    def __str__(self):
        return "{} ({}) ({})".format(self.usuario.first_name,self.tipo,self.data)
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
    
