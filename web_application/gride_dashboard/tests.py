from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import *
import datetime

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
        dadoIntegridade = DadosIntegridade(self.user, 91.9, 92.9)
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

        #create
        DadosFalha.objects.get(usuario=self.user)    
        dadoFalha = DadosFalha(self.user, 'falha')
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

        #create
        DadosDesempenho.objects.get(usuario=self.user)   
        dadoDesempenho = DadosDesempenho(self.user, 91.9, 92.9, 93.9, 94.9, 95.9, 96.9, 97.9, 98.9)
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

        #create
        CacheRelatorio.objects.get(usuario=self.user)    
        cache = CacheRelatorio(self.user, 'cache', '{}', datetime(2015, 10, 9, 23, 55, 59, 342380), datetime(2015, 10, 9, 23, 55, 59, 342380))
        cache.save()
        #read
        cache = CacheRelatorio.objects.get(usuario=self.user)
        self.assertEqual(cache.tipo, 'cache')
        self.assertEqual(cache.dados_relatorio, '{}')
        self.assertEqual(cache.inicio_periodo, datetime(2015, 10, 9, 23, 55, 59, 342380))
        self.assertEqual(cache.fim_periodo, datetime(2015, 10, 9, 23, 55, 59, 342380))
        #update
        cache.tipo = 'cache2'
        cache.save()
        self.assertEqual(cache.tipo, 'cache2')
        #delete
        cache.delete()

class URLTest(TestCase):
    def testURL(self):
        c = Client()
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/index/")
        self.assertEqual(response.status_code, 200)
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
        response = self.client.get("/proxy-cache/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/users-profile/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/pages-contact/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/read_user/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/update_user/")
        self.assertEqual(response.status_code, 200)

        