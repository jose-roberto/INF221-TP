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
from gride_dashboard.projecao_produtiva.projecao_produtiva import ProjecaoProdutiva
from numpy import asarray

# Create your views here.
class IndexView(TemplateView):
    template_name='index.html'
class HomepageView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='homepage.html'
class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='users-profile.html'
class ContactView(LoginRequiredMixin, TemplateView):
    login_url = 'pages-login'
    template_name='pages-contact.html'

@login_required
def proxyView(request):
    user = request.user
    
    _data_inicio = request.POST.get('data_inicio')
    _data_termino = request.POST.get('data_termino')
    tipo = request.POST.get('tipo')
    
    cache = CacheRelatorio.objects.filter(usuario=request.user).filter(tipo=tipo).filter(inicio_periodo=_data_inicio).filter(fim_periodo=_data_termino)
    if len(cache) != 0:
        generator = PDFGenerator()
        data_inicio =  _data_inicio[8:11] + "/" + _data_inicio[5:7] + "/" + _data_inicio[0:4]
        data_termino =  _data_termino[8:11] + "/" + _data_termino[5:7] + "/" + _data_termino[0:4]
        
        if tipo == 'Integridade':
            header = ["Data", "Efiencia Placa", "Integridade Placa"]
            pdf = generator.create_report(cache[0].dados_relatorio, "Relatório de Integridade", header, (data_inicio, data_termino), user.username)
        elif tipo == 'Falhas':
            header = ["Data", "Descrição Falha"]
            pdf = generator.create_report(cache[0].dados_relatorio, "Relatório de Falhas", header, (data_inicio, data_termino), request.user.username)
        elif tipo == 'Produção':
            header = ["Data", "Producao(kw)", "Consumo(kw)", "Lucro(kw)", "Lucro($)"]
            pdf = generator.create_report(cache[0].dados_relatorio, "Relatório de Produção", header, (data_inicio, data_termino), request.user.username)
        elif tipo == 'Projecão Produtiva':
            header = ["Data", "Producao(kw)", "Consumo(kw)", "Lucro(kw)", "Lucro($)"]
            pdf = generator.create_report(cache[0].dados_relatorio, "Projeção Produtiva", header, (data_inicio, data_termino), request.user.username)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        return response
    else:
        if tipo == 'Integridade':
            return integridyView(request)
        elif tipo == 'Falhas':
            return failureView(request)
        elif tipo == 'Produção':
            return productionView(request)
        elif tipo == 'Projecão Produtiva':
            return projectionView(request)

@login_required
def integridyView(request):
    if request.method == "GET":
        return render(request,'report-integridy.html')
    else:
        _data_inicio = request.POST.get('data_inicio')
        _data_termino = request.POST.get('data_termino')
        filterList = DadosIntegridade.objects.filter(usuario=request.user).filter(data__gte=_data_inicio).filter(data__lte=_data_termino)
        
        data_list = []
        for item in filterList:
            data_list.append([item.data.strftime('%d/%m/%Y'), item.eficiencia_placa, item.integridade_placa])
        
        generator = PDFGenerator()
        header = ["Data", "Efiencia Placa", "Integridade Placa"]
        data_inicio =  _data_inicio[8:11] + "/" + _data_inicio[5:7] + "/" + _data_inicio[0:4]
        data_termino =  _data_termino[8:11] + "/" + _data_termino[5:7] + "/" + _data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Integridade", header, (data_inicio, data_termino), request.user.username)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        
        user = request.user
        _usuario = User.objects.filter(username=user.username)
        
        relatorio_integridade = CacheRelatorio(usuario = _usuario[0], tipo='Integridade', dados_relatorio=data_list, inicio_periodo = _data_inicio, fim_periodo = _data_termino)
        relatorio_integridade.save()
        
        return response

@login_required
def failureView(request):
    if request.method == "GET":
        return render(request,'report-failure.html')
    else:
        _data_inicio = request.POST.get('data_inicio')
        _data_termino = request.POST.get('data_termino')
        filterList = DadosFalha.objects.filter(usuario=request.user).filter(data__gte=_data_inicio).filter(data__lte=_data_termino)
        
        data_list = []
        for item in filterList:
            data_list.append([item.data.strftime('%d/%m/%Y'), item.falha])
        
        generator = PDFGenerator()
        header = ["Data", "Descrição Falha"]
        data_inicio =  _data_inicio[8:11] + "/" + _data_inicio[5:7] + "/" + _data_inicio[0:4]
        data_termino =  _data_termino[8:11] + "/" + _data_termino[5:7] + "/" + _data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Falhas", header, (data_inicio, data_termino), request.user.username)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        
        user = request.user
        _usuario = User.objects.filter(username=user.username)
        
        relatorio_falhas = CacheRelatorio(
            usuario=_usuario[0], 
            tipo='Falhas', 
            dados_relatorio=data_list,
            inicio_periodo=_data_inicio, 
            fim_periodo=_data_termino
        )
        relatorio_falhas.save()
        
        return response
        
@login_required
def productionView(request):
    if request.method == "GET":
        return render(request,'report-production.html')
    else:
        _data_inicio = request.POST.get('data_inicio')
        _data_termino = request.POST.get('data_termino')
        filterList = DadosDesempenho.objects.filter(usuario=request.user).filter(data__gte=_data_inicio).filter(data__lte=_data_termino)
        
        data_list = []
        for item in filterList:
            value = item.producao_energetica - item.consumo_energetico
            data_list.append([item.data.strftime('%d/%m/%Y'), item.producao_energetica, item.consumo_energetico, 
                              value, value * item.valor_kwh])
        
        generator = PDFGenerator()
        header = ["Data", "Producao(kw)", "Consumo(kw)", "Lucro(kw)", "Lucro($)"]
        data_inicio =  _data_inicio[8:11] + "/" + _data_inicio[5:7] + "/" + _data_inicio[0:4]
        data_termino =  _data_termino[8:11] + "/" + _data_termino[5:7] + "/" + _data_termino[0:4]
        pdf = generator.create_report(data_list, "Relatório de Produção", header, (data_inicio, data_termino), request.user.username)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        
        user = request.user
        _usuario = User.objects.filter(username=user.username)
        
        relatorio_producao = CacheRelatorio(usuario = _usuario[0], tipo='Produção', dados_relatorio=data_list, inicio_periodo = _data_inicio, fim_periodo = _data_termino)
        relatorio_producao.save()
        
        return response

@login_required 
def projectionView(request):
    if request.method == "GET":
        return render(request,'projection.html')
    else:
        _data_inicio = request.POST.get('data_inicio')
        _data_termino = request.POST.get('data_termino')
        crescimento = request.POST.get('crescimento')
        crescimento = int(crescimento)/100
        
        mes_inicio = int(_data_inicio[5:7])
        dia_inicio = int(_data_inicio[8:10])
        mes_termino = int(_data_termino[5:7])
        dia_termino = int(_data_termino[8:10])

        filterList = DadosDesempenho.objects.filter(
            usuario=request.user,
            data__month__gte=mes_inicio,
            data__month__lte=mes_termino,
            data__day__gte=dia_inicio,
            data__day__lte=dia_termino
        )
        
        proj = ProjecaoProdutiva(crescimento)
        
        data_list = []
        for item in filterList:
            data_list.append([item.data.strftime('%d/%m/%Y'), item.producao_energetica, item.consumo_energetico, item.valor_kwh])
        
        data_proj = proj.projecao_produtiva(data_list)
        
        generator = PDFGenerator()
        header = ["Data", "Producao(kw)", "Consumo(kw)", "Lucro(kw)", "Lucro($)"]
        data_inicio =  _data_inicio[8:11] + "/" + _data_inicio[5:7] + "/" + _data_inicio[0:4]
        data_termino =  _data_termino[8:11] + "/" + _data_termino[5:7] + "/" + _data_termino[0:4]
        pdf = generator.create_report(data_proj, "Projeção Produtiva", header, (data_inicio, data_termino), request.user.username)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
        
        user = request.user
        _usuario = User.objects.filter(username=user.username)
        
        relatorio_projecao = CacheRelatorio(usuario = _usuario[0], tipo='Projecão Produtiva', dados_relatorio=data_list, inicio_periodo = _data_inicio, fim_periodo = _data_termino)
        relatorio_projecao.save()
        
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

    usuario = Usuario.objects.filter(cnpj=User.objects.filter(username=user.username)[0].username)
    
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
        usuario = Usuario.objects.filter(cnpj=User.objects.filter(username=user.username)[0].username)

        usuario.update(nome = request.POST.get('name'), email = request.POST.get('email'), telefone = request.POST.get('phone'), localizacao = request.POST.get('location'))
        
        return redirect('read_user')

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
    fields = ['tipo', 'dados_relatorio', 'inicio_periodo', 'fim_periodo',]
    template_name = 'forms/cadastro.html'
    success_url = reverse_lazy('list-cache-relatorio')
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)
class UpdateCacheRelatorio(UpdateView):
    model = CacheRelatorio
    fields = ['tipo', 'dados_relatorio', 'inicio_periodo', 'fim_periodo',]
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

    
