from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Usuario

from gride_dashboard.projecao_produtiva.projecao_produtiva import projecao_produtiva

from numpy import asarray

# Create your views here.
@login_required(login_url='/pages-login.html')
def homepage(request):
    return render(request,'homepage.html')

def index(request):
    return render(request,'index.html')

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
        
        return redirect("index.html")

def login(request):
    if request.method == "GET":
        return render(request,'pages-login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            django_login(request, user)
            
            return redirect('homepage.html')
       
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
 
def consumption(request):
    return render(request,'report-consumption.html')

def integridy(request):
    return render(request,'report-integridy.html')

def failure(request):
    return render(request,'report-failure.html')

def production(request):
    return render(request,'report-production.html')

def projection(request):
    return render(request,'projection.html')

def profile(request):
    return render(request, 'users-profile.html')

def contact(request):
    return render(request, 'pages-contact.html')

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
