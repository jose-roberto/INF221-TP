from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from gride_dashboard.projecao_produtiva.projecao_produtiva import projecao_produtiva

from numpy import asarray

# Create your views here.
def index(request):
    #return HttpResponse("Hello, world. You're at the gride_dashboard index.")
    return render(request,'index.html')

def consumption(request):
    #return HttpResponse("Hello, world. You're at the gride_dashboard index.")
    return render(request,'report-consumption.html')

def integridy(request):
    #return HttpResponse("Hello, world. You're at the gride_dashboard index.")
    return render(request,'report-integridy.html')

def failure(request):
    #return HttpResponse("Hello, world. You're at the gride_dashboard index.")
    return render(request,'report-failure.html')

def production(request):
    #return HttpResponse("Hello, world. You're at the gride_dashboard index.")
    return render(request,'report-production.html')

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
