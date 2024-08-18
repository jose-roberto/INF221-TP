from django.db.models.query import QuerySet
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
from django.contrib.auth.mixins import LoginRequiredMixin

from gride_dashboard.pdf.pdf_generator import PDFGenerator
from gride_dashboard.projecao_produtiva.projecao_produtiva import projecao_produtiva
from numpy import asarray

# Create your views here.
class IndexView(TemplateView):
    template_name='index.html'
class HomepageView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='homepage.html'
class ProjectionView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='projection.html'
class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='users-profile.html'
class ContactView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='pages-contact.html'

@login_required
def integridyView(request):
    if request.method == "GET":
        return render(request,'report-integridy.html')
    else:
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        filterList = DadosIntegridade.objects.filter(usuario=request.user).filter(data__gte=data_inicio).filter(data__lte=data_termino)
        
        data_list = []
        for item in filterList:
            data_list.append([item.data.strftime('%d/%m/%Y'), item.eficiencia_placa, item.integridade_placa])
        
        generator = PDFGenerator()
        header = ["Data", "Efiencia Placa", "Integridade Placa"]
        data_inicio =  data_inicio[8:11] + "/" + data_inicio[5:7] + "/" + data_inicio[0:4]
        data_termino =  data_termino[8:11] + "/" + data_termino[5:7] + "/" + data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Integridade", header, (data_inicio, data_termino), "Wiliam Ltda.")
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        return response

@login_required
def failureView(request):
    if request.method == "GET":
        return render(request,'report-failure.html')
    else:
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        filterList = DadosFalha.objects.filter(usuario=request.user).filter(data__gte=data_inicio).filter(data__lte=data_termino)
        
        data_list = []
        for item in filterList:
            data_list.append([item.data.strftime('%d/%m/%Y'), item.falha])
        
        generator = PDFGenerator()
        header = ["Data", "Descrição Falha"]
        data_inicio =  data_inicio[8:11] + "/" + data_inicio[5:7] + "/" + data_inicio[0:4]
        data_termino =  data_termino[8:11] + "/" + data_termino[5:7] + "/" + data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Falhas", header, (data_inicio, data_termino), "Wiliam Ltda.")
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        return response
        
@login_required
def productionView(request):
    if request.method == "GET":
        return render(request,'report-production.html')
    else:
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        filterList = DadosDesempenho.objects.filter(usuario=request.user).filter(data__gte=data_inicio).filter(data__lte=data_termino)
        
        data_list = []
        for item in filterList:
            value = item.producao_energetica - item.consumo_energetico
            data_list.append([item.data.strftime('%d/%m/%Y'), item.producao_energetica, item.consumo_energetico, 
                              value, value * item.valor_kwh])
        
        generator = PDFGenerator()
        header = ["Data", "Producao(kw)", "Consumo(kw)", "Lucro(kw)", "Lucro($)"]
        data_inicio =  data_inicio[8:11] + "/" + data_inicio[5:7] + "/" + data_inicio[0:4]
        data_termino =  data_termino[8:11] + "/" + data_termino[5:7] + "/" + data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Produção", header, (data_inicio, data_termino), "Wiliam Ltda.")
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        return response

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
    
@login_required
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
    fields = ['integridade_placa', 'eficiencia_placa',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-dados-integridade')
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
class UpdateDadosIntegridade(UpdateView):
    model = DadosIntegridade
    fields = ['integridade_placa', 'eficiencia_placa',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-dados-integridade')
class DeleteDadosIntegridade(DeleteView):
    model = DadosIntegridade
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-dados-integridade')
class ListDadosIntegridade(ListView):
    model = DadosIntegridade
    template_name = 'forms/list-dados-integridade.html'
    def get_queryset(self):
        self.object_list = DadosIntegridade.objects.filter(usuario=self.request.user)
        return self.object_list
        
class CreateDadosFalhas(CreateView):
    model = DadosFalha
    fields = ['falha',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-dados-falhas')
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
class UpdateDadosFalhas(UpdateView):
    model = DadosFalha
    fields = ['falha',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-dados-falhas')
class DeleteDadosFalhas(DeleteView):
    model = DadosFalha
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-dados-falhas')
class ListDadosFalhas(ListView):
    model = DadosFalha
    template_name = 'forms/list-dados-falhas.html'

    def get_queryset(self):
        self.object_list = DadosFalha.objects.filter(usuario=self.request.user)
        return self.object_list

class CreateDadosDesempenho(CreateView):
    model = DadosDesempenho
    fields = [
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
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
class UpdateDadosDesempenho(UpdateView):
    model = DadosDesempenho
    fields = [
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
    def get_queryset(self):
        self.object_list = DadosDesempenho.objects.filter(usuario=self.request.user)
        return self.object_list
    
class CreateCacheRelatorio(CreateView):
    model = CacheRelatorio
    fields = ['tipo', 'dados_relatorio',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-cache-relatorio')
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
class UpdateCacheRelatorio(UpdateView):
    model = CacheRelatorio
    fields = ['tipo', 'dados_relatorio',]
    template_name = 'forms/update.html'
    success_url = reverse_lazy('list-cache-relatorio')
class DeleteCacheRelatorio(DeleteView):
    model = CacheRelatorio
    template_name = 'forms/delete.html'
    success_url = reverse_lazy('list-cache-relatorio')
class ListCacheRelatorio(ListView):
    model = CacheRelatorio
    template_name = 'forms/list-cache-relatorio.html'
    def get_queryset(self):
        self.object_list = CacheRelatorio.objects.filter(usuario=self.request.user)
        return self.object_list

    
