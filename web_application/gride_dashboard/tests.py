from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import *
from .views import getDados, getDadosProj
from datetime import datetime
User = get_user_model()
# Create your tests here.

class RegisterTest(TestCase):
    def testRegister(self):
        c = Client()
        response = c.get("/pages-register/")
        self.assertEqual(response.status_code, 200) #load page
        response = c.post("/pages-register/", 
                            {"name":"testRegister",
                            "email":"testregister@testregister.com",
                            "username":"99999999999999",
                            "password":"testPassword",
                            "phone":"9999999999",
                            "location":"testLocation",
                            "terms":"on"})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/index/')  #redirect to /index/
        testUser=User.objects.get(username="99999999999999")
        self.assertEqual(testUser.email,'testregister@testregister.com')
        self.assertEqual(testUser.first_name,'testRegister')
        testUsuario=Usuario.objects.get(cnpj="99999999999999")
        self.assertEqual(testUsuario.nome,'testRegister')
        self.assertEqual(testUsuario.email,'testregister@testregister.com')
        self.assertEqual(testUsuario.telefone,'9999999999')
        self.assertEqual(testUsuario.localizacao,'testLocation')
class LoginTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.client.post("/pages-register/", 
                {"name":"testRegister",
                "email":"testregister@testregister.com",
                "username":"99999999999999",
                "password":"testPassword",
                "phone":"9999999999",
                "location":"testLocation",
                "terms":"on"})
        cls.user=User.objects.get(username="99999999999999")
        cls.usuario=Usuario.objects.get(cnpj="99999999999999")
    def testLoginFail(self):
        #usuario errado
        response = self.client.get("/pages-login/")
        self.assertEqual(response.status_code, 200) #load page
        response = self.client.post("/pages-login/", 
                            {"username":"19999999999999",
                            "password":"testPassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha inválidos')  #HttpResponse
        #senha errada
        response = self.client.get("/pages-login/")
        self.assertEqual(response.status_code, 200) #load page
        response = self.client.post("/pages-login/", 
                            {"username":"99999999999999",
                            "password":"wrongPassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha inválidos')  #HttpResponse
    def testLoginSuccess(self):
        response = self.client.get("/pages-login/")
        self.assertEqual(response.status_code, 200) #load page
        response = self.client.post("/pages-login/", 
                                    {"username":"99999999999999",
                                    "password":"testPassword"})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/homepage/')  #redirect to /homepage/
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200) #load page
        
    def testLogout(self):
        self.client.force_login(self.user)  
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index/')  #redirect to /index/
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/pages-login/?next=/homepage/')  #redirect to /pages-login/
class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.client.post("/pages-register/", 
                {"name":"testRegister",
                "email":"testregister@testregister.com",
                "username":"99999999999999",
                "password":"testPassword",
                "phone":"9999999999",
                "location":"testLocation",
                "terms":"on"})
        cls.user=User.objects.get(username="99999999999999")
        cls.usuario=Usuario.objects.get(cnpj="99999999999999")
    def setUp(self):
        self.client.force_login(self.user)  
    def testReadUser(self):
        response = self.client.get("/read_user/")
        self.assertEqual(response.status_code, 200) #load page
        context = response.context
        self.assertEqual(context['name'], self.usuario.nome)
        self.assertEqual(context['username'], self.usuario.cnpj)
        self.assertEqual(context['email'], self.usuario.email)
        self.assertEqual(context['phone'], self.usuario.telefone)
        self.assertEqual(context['location'], self.usuario.localizacao)
    def testUpdateUser(self):
        response = self.client.post("/update_user/", 
                                    {"name":"newRegister",
                                    "email":"newregister@testregister.com",
                                    "phone":"1999999999",
                                    "location":"newLocation"})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/read_user/')  #redirect to /read_user/
        self.usuario=Usuario.objects.get(cnpj="99999999999999")
        self.assertEqual(self.usuario.nome,'newRegister')
        self.assertEqual(self.usuario.email,'newregister@testregister.com')
        self.assertEqual(self.usuario.telefone,'1999999999')
        self.assertEqual(self.usuario.localizacao,'newLocation')
    def testCRUD(self):
        #create
        dadoIntegridade = DadosIntegridade(usuario=self.user, 
                                           integridade_placa=91.9, 
                                           eficiencia_placa=92.9)
        dadoIntegridade.save()
        #read
        dadoIntegridade = DadosIntegridade.objects.get(usuario=self.user)
        self.assertEqual(dadoIntegridade.integridade_placa, 91.9)
        self.assertEqual(dadoIntegridade.eficiencia_placa, 92.9)
        #update
        dadoIntegridade.integridade_placa = 93.9
        dadoIntegridade.save()
        self.assertEqual(dadoIntegridade.integridade_placa, 93.9)
        #delete
        dadoIntegridade.delete()
        with self.assertRaises(DadosIntegridade.DoesNotExist):
            dadoIntegridade = DadosIntegridade.objects.get(usuario=self.user)

        #create
        dadoFalha = DadosFalha(usuario=self.user, falha='falha')
        dadoFalha.save()
        #read
        dadoFalha = DadosFalha.objects.get(usuario=self.user)
        self.assertEqual(dadoFalha.falha, 'falha')
        #update
        dadoFalha.falha = 'falha2'
        dadoFalha.save()
        self.assertEqual(dadoFalha.falha, 'falha2')
        #delete
        dadoFalha.delete()
        with self.assertRaises(DadosFalha.DoesNotExist):
            dadoFalha = DadosFalha.objects.get(usuario=self.user)

        #create
        dadoDesempenho = DadosDesempenho(usuario=self.user, 
                                         producao_energetica=91.9, 
                                         consumo_energetico=92.9, 
                                         valor_kwh=93.9, lucro=94.9, 
                                         prejuizo=95.9, margem=96.9, 
                                         tempo_de_operacao=97.9, 
                                         tempo_de_parada=98.9)
        dadoDesempenho.save()
        #read
        dadoDesempenho = DadosDesempenho.objects.get(usuario=self.user)
        self.assertEqual(dadoDesempenho.producao_energetica, 91.9)
        self.assertEqual(dadoDesempenho.consumo_energetico, 92.9)
        self.assertEqual(dadoDesempenho.valor_kwh, 93.9)    
        self.assertEqual(dadoDesempenho.lucro, 94.9)
        self.assertEqual(dadoDesempenho.prejuizo, 95.9)
        self.assertEqual(dadoDesempenho.margem, 96.9)
        self.assertEqual(dadoDesempenho.tempo_de_operacao, 97.9)
        self.assertEqual(dadoDesempenho.tempo_de_parada, 98.9)
        #update
        dadoDesempenho.producao_energetica = 99.9
        dadoDesempenho.save()
        self.assertEqual(dadoDesempenho.producao_energetica, 99.9)
        #delete
        dadoDesempenho.delete()
        with self.assertRaises(DadosDesempenho.DoesNotExist):
            dadoDesempenho = DadosDesempenho.objects.get(usuario=self.user)

        #create
        cache = CacheRelatorio(usuario=self.user, 
                               tipo='cache',
                               dados_relatorio='{}', 
                               inicio_periodo=datetime(2015, 10, 10), 
                               fim_periodo=datetime(2015, 10, 10))
        cache.save()
        #read
        cache = CacheRelatorio.objects.get(usuario=self.user)
        self.assertEqual(cache.tipo, 'cache')
        self.assertEqual(cache.dados_relatorio, '{}')
        self.assertEqual(cache.inicio_periodo.strftime("%m/%d/%Y"), '10/10/2015')
        self.assertEqual(cache.fim_periodo.strftime("%m/%d/%Y"), '10/10/2015')
        #update
        cache.tipo = 'cache2'
        cache.save()
        self.assertEqual(cache.tipo, 'cache2')
        #delete
        cache.delete()
        with self.assertRaises(CacheRelatorio.DoesNotExist):
            cache = CacheRelatorio.objects.get(usuario=self.user)
    def testRelatorio(self):
        response = self.client.post("/report-integridy/", 
                                    {"data_inicio":"2024-08-01",
                                    "data_termino":"2024-08-02"})
        self.assertEqual(response.status_code, 200)
        ## TESTA CACHE
        _data_inicio = datetime(2024, 8, 1, 0, 0, 0, 0)
        _data_termino = datetime(2024, 8, 2, 23, 59, 59, 0)
        filterList = CacheRelatorio.objects.filter(usuario=self.user).filter(tipo='Integridade').filter(inicio_periodo=_data_inicio).filter(fim_periodo=_data_termino)
        self.assertGreater(len(filterList), 0)
        ##
        response = self.client.post("/report-failure/", 
                                    {"data_inicio":"2024-08-01",
                                    "data_termino":"2024-08-02"})
        self.assertEqual(response.status_code, 200)
        ## TESTA CACHE 
        _data_inicio = datetime(2024, 8, 1, 0, 0, 0, 0)
        _data_termino = datetime(2024, 8, 2, 23, 59, 59, 0)
        filterList = CacheRelatorio.objects.filter(usuario=self.user).filter(tipo='Falhas').filter(inicio_periodo=_data_inicio).filter(fim_periodo=_data_termino)
        self.assertGreater(len(filterList), 0)
        ##
        response = self.client.post("/report-production/", 
                                    {"data_inicio":"2024-08-01",
                                    "data_termino":"2024-08-02"})
        self.assertEqual(response.status_code, 200) 
        ## TESTA CACHE
        _data_inicio = datetime(2024, 8, 1, 0, 0, 0, 0)
        _data_termino = datetime(2024, 8, 2, 23, 59, 59, 0)
        filterList = CacheRelatorio.objects.filter(usuario=self.user).filter(tipo='Produção').filter(inicio_periodo=_data_inicio).filter(fim_periodo=_data_termino)
        self.assertGreater(len(filterList), 0)
        ##
        response = self.client.post("/projection/", 
                                    {"data_inicio":"2024-08-01",
                                    "data_termino":"2024-08-03",
                                    "crescimento":10})
        self.assertEqual(response.status_code, 200) 
        ## TESTA CACHE
        _data_inicio = datetime(2024, 8, 1, 0, 0, 0, 0)
        _data_termino = datetime(2024, 8, 3, 23, 59, 59, 0)
        filterList = CacheRelatorio.objects.filter(usuario=self.user).filter(tipo='Projecão Produtiva').filter(inicio_periodo=_data_inicio).filter(fim_periodo=_data_termino)
        self.assertGreater(len(filterList), 0)
        ##

        dadoIntegridade1 = DadosIntegridade(usuario=self.user,
                                           data=datetime(2024, 8, 1, 0, 0, 0, 0), 
                                           integridade_placa=91.9, 
                                           eficiencia_placa=92.9)
        dadoIntegridade1.save()
        dadoIntegridade2 = DadosIntegridade(usuario=self.user,
                                           data=datetime(2024, 8, 2, 0, 0, 0, 0), 
                                           integridade_placa=91.9, 
                                           eficiencia_placa=92.9)
        dadoIntegridade2.save()
        dadoIntegridade3 = DadosIntegridade(usuario=self.user,
                                           data=datetime(2024, 8, 3, 12, 0, 0, 0), 
                                           integridade_placa=91.9, 
                                           eficiencia_placa=92.9)
        dadoIntegridade3.save()
        filterList=getDados(self.user, 'Integridade', datetime(2024, 8, 1, 12, 0, 0, 0), datetime(2024, 8, 3, 12, 0, 0, 0))
        self.assertEqual(len(filterList), 2)
        self.assertFalse(dadoIntegridade1 in filterList)
        self.assertTrue(dadoIntegridade2 in filterList)
        self.assertTrue(dadoIntegridade3 in filterList)
        filterList=getDados(self.user, 'Integridade', datetime(2024, 8, 3, 13, 0, 0, 0), datetime(2024, 9, 15, 0, 0, 0, 0))
        self.assertEqual(len(filterList), 0)

        dadoFalha1 = DadosFalha(usuario=self.user,
                                data=datetime(2024, 8, 1, 0, 0, 0, 0), 
                                falha='falha1')
        dadoFalha1.save()
        dadoFalha2 = DadosFalha(usuario=self.user,
                                data=datetime(2024, 8, 2, 0, 0, 0, 0), 
                                falha='falha2')
        dadoFalha2.save()
        dadoFalha3 = DadosFalha(usuario=self.user,
                                data=datetime(2024, 8, 3, 12, 0, 0, 0), 
                                falha='falha3')
        dadoFalha3.save()
        filterList=getDados(self.user, 'Falhas', datetime(2024, 8, 1, 12, 0, 0, 0), datetime(2024, 8, 3, 12, 0, 0, 0))
        self.assertEqual(len(filterList), 2)
        self.assertFalse(dadoFalha1 in filterList)
        self.assertTrue(dadoFalha2 in filterList)
        self.assertTrue(dadoFalha3 in filterList)
        filterList=getDados(self.user, 'Falhas', datetime(2024, 8, 3, 13, 0, 0, 0), datetime(2024, 9, 15, 0, 0, 0, 0))
        self.assertEqual(len(filterList), 0)

        dadoDesempenho1 = DadosDesempenho(usuario=self.user,
                                        data=datetime(2024, 8, 1, 0, 0, 0, 0), 
                                        producao_energetica=91.9, 
                                         consumo_energetico=92.9, 
                                         valor_kwh=93.9, lucro=94.9, 
                                         prejuizo=95.9, margem=96.9, 
                                         tempo_de_operacao=97.9, 
                                         tempo_de_parada=98.9)
        dadoDesempenho1.save()
        dadoDesempenho2 = DadosDesempenho(usuario=self.user,
                                        data=datetime(2024, 8, 2, 0, 0, 0, 0), 
                                        producao_energetica=91.9, 
                                         consumo_energetico=92.9, 
                                         valor_kwh=93.9, lucro=94.9, 
                                         prejuizo=95.9, margem=96.9, 
                                         tempo_de_operacao=97.9, 
                                         tempo_de_parada=98.9)
        dadoDesempenho2.save()
        dadoDesempenho3 = DadosDesempenho(usuario=self.user,
                                        data=datetime(2024, 8, 3, 12, 0, 0, 0), 
                                        producao_energetica=91.9, 
                                         consumo_energetico=92.9, 
                                         valor_kwh=93.9, lucro=94.9, 
                                         prejuizo=95.9, margem=96.9, 
                                         tempo_de_operacao=97.9, 
                                         tempo_de_parada=98.9)
        dadoDesempenho3.save()
        filterList=getDados(self.user, 'Produção', datetime(2024, 8, 1, 12, 0, 0, 0), datetime(2024, 8, 3, 12, 0, 0, 0))
        self.assertEqual(len(filterList), 2)
        self.assertFalse(dadoDesempenho1 in filterList)
        self.assertTrue(dadoDesempenho2 in filterList)
        self.assertTrue(dadoDesempenho3 in filterList)
        filterList=getDados(self.user, 'Produção', datetime(2024, 8, 3, 13, 0, 0, 0), datetime(2024, 9, 15, 0, 0, 0, 0))
        self.assertEqual(len(filterList), 0)
    def testURL(self):
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/report-failure/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/report-integridy/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/report-production/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/projection/")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/proxy-cache/", {
            'data_inicio': '2023-01-01',
            'data_termino': '2023-01-02',
            'tipo': 'Integridade'
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/users-profile/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/pages-contact/")
        self.assertEqual(response.status_code, 200)
        
class LogoutURLTest(TestCase):
    def testURL(self):
        c = Client()
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/homepage/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/homepage/')  #redirect to /pages-login/
        response = self.client.get("/report-failure/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/report-failure/')  #redirect to /pages-login/
        response = self.client.get("/report-integridy/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/report-integridy/')  #redirect to /pages-login/
        response = self.client.get("/report-production/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/report-production/')  #redirect to /pages-login/
        response = self.client.get("/projection/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/projection/')  #redirect to /pages-login/
        response = self.client.get("/proxy-cache/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/proxy-cache/')  #redirect to /pages-login/
        response = self.client.get("/users-profile/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/users-profile/')  #redirect to /pages-login/
        response = self.client.get("/pages-contact/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/pages-contact/')  #redirect to /pages-login/
        response = self.client.get("/read_user/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/read_user/')  #redirect to /pages-login/
        response = self.client.get("/update_user/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/pages-login/?next=/update_user/')  #redirect to /pages-login/
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index/')  #redirect to /pages-login/


        