from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import *
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
        pass
    
    def testLoginSuccess(self):
        response = self.client.get("/pages-login/")
        self.assertEqual(response.status_code, 200) #load page
        response = self.client.post("/pages-login/", 
                                    {"username":"99999999999999",
                                    "password":"testPassword"})
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, '/homepage/')  #redirect to /homepage/
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
        c = Client()
        response = self.client.get("/pages-login/")
        self.assertEqual(response.status_code, 200) #load page
        response = self.client.post("/pages-login/", 
                            {"username":"99999999999999",
                            "password":"wrongPassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuário ou senha inválidos')  #HttpResponse
    def testLogout(self):
        c = Client()
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/index/')  #redirect to /index/

