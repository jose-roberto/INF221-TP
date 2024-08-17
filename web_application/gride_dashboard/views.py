from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy

from gride_dashboard.projecao_produtiva.projecao_produtiva import projecao_produtiva

from numpy import asarray

# Create your views here.
#@login_required(login_url='/pages-login.html')
class HomepageView(TemplateView):
    template_name='homepage.html'
class IndexView(TemplateView):
    template_name='index.html'
class ConsumptionView(TemplateView):
    template_name='report-consumption.html'
class IntegridyView(TemplateView):
    template_name='report-integridy.html'
class FailureView(TemplateView):
    template_name='report-failure.html'
class ProductionView(TemplateView):
    template_name='report-production.html'
class ProjectionView(TemplateView):
    template_name='projection.html'
class ProfileView(TemplateView):
    template_name='users-profile.html'
class ContactView(TemplateView):
    template_name='pages-contact.html'

def register(request):
    if request.method == "GET":
        return render(request,'pages-register.html')
    else:
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        
        user_verification = User.objects.filter(username=username).first()
        
        if user_verification:
            return HttpResponse(f"Usuário {username} já existe")
        
        new_user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        new_user.save()
        
        usuario = Usuario(cnpj=username, nome=name, email=email, senha=password, localizacao=location, telefone=phone)
        usuario.save()
        
        return redirect('index')

def login(request):
    if request.method == "GET":
        return render(request,'pages-login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            django_login(request, user)
            
            return redirect('homepage')
       
        return HttpResponse("Usuário ou senha inválidos")
    
def logout(request):
    django_logout(request)

    return redirect('index')

@login_required
def read_user(request):
    user = request.user
    usuario = Usuario.objects.filter(cnpj=user.username)
   
    context = {
        'name': usuario[0].nome,
        'username': usuario[0].cnpj,
        'email': usuario[0].email,
        'phone': usuario[0].telefone,
        'location': usuario[0].localizacao
    }
    
    return render(request, 'users-profile.html', context)

@login_required
def update_user(request):
    if request.method == "POST":
        user = request.user
        usuario = Usuario.objects.filter(cnpj=user.username)
        
        usuario[0].nome = request.POST.get('name')
        usuario[0].email = request.POST.get('email')
        usuario[0].telefone = request.POST.get('phone')
        usuario[0].localizacao = request.POST.get('location')
        
        usuario[0].save()
        
        return redirect('read_user')

def render_projecao_produtiva(request):
    try:
        response = projecao_produtiva(request)
        if isinstance(response, JsonResponse):
            data = response.json()
            data = asarray(data)
        else:
            return response
    except ValueError as e:
        return HttpResponse(f"Erro ao processar os dados: {e}")
    except Exception as e:
        return HttpResponse(f"Erro inesperado: {e}")
    
    return render(request, 'projecao_produtiva.html', {'data': data})

class CreateDadosIntegridade(CreateView):
    model = DadosIntegridade
    fields = ['usuario', 'integridade_placa', 'eficiencia_placa',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-dados-integridade')
class UpdateDadosIntegridade(UpdateView):
    model = DadosIntegridade
    fields = ['usuario', 'integridade_placa', 'eficiencia_placa',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-dados-integridade')
class DeleteDadosIntegridade(DeleteView):
    model = DadosIntegridade
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-dados-integridade')
class ListDadosIntegridade(ListView):
    model = DadosIntegridade
    template_name = 'forms/list-dados-integridade.html'
        
class CreateDadosFalhas(CreateView):
    model = DadosFalhas
    fields = ['usuario', 'falha',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-dados-falhas')
class UpdateDadosFalhas(UpdateView):
    model = DadosFalhas
    fields = ['usuario', 'falha',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-dados-falhas')
class DeleteDadosFalhas(DeleteView):
    model = DadosFalhas
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-dados-falhas')
class ListDadosFalhas(ListView):
    model = DadosFalhas
    template_name = 'forms/list-dados-falhas.html'

class CreateDadosDesempenho(CreateView):
    model = DadosDesempenho
    fields = ['usuario', 
              'producao_energetica',
              'consumo_energetico',
              'valor_kwh',
              'lucro',
              'prejuizo',
              'margem',
              'tempo_de_operacao',
              'tempo_de_parada', 
              ]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-dados-desempenho')
class UpdateDadosDesempenho(UpdateView):
    model = DadosDesempenho
    fields = ['usuario', 
              'producao_energetica',
              'consumo_energetico',
              'valor_kwh',
              'lucro',
              'prejuizo',
              'margem',
              'tempo_de_operacao',
              'tempo_de_parada', 
              ]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-dados-desempenho')
class DeleteDadosDesempenho(DeleteView):
    model = DadosDesempenho
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-dados-desempenho')
class ListDadosDesempenho(ListView):
    model = DadosDesempenho
    template_name = 'forms/list-dados-desempenho.html'
    
class CreateCacheRelatorio(CreateView):
    model = CacheRelatorio
    fields = ['usuario', 'tipo', 'dados_relatorio',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-cache-relatorio')
class UpdateCacheRelatorio(UpdateView):
    model = CacheRelatorio
    fields = ['usuario', 'tipo', 'dados_relatorio',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-cache-relatorio')
class DeleteCacheRelatorio(DeleteView):
    model = CacheRelatorio
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-cache-relatorio')
class ListCacheRelatorio(ListView):
    model = CacheRelatorio
    template_name = 'forms/list-cache-relatorio.html'

    
