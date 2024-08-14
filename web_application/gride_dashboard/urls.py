from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage.html', views.homepage, name='homepage'),
    path('pages-register.html', views.register, name='pages-register'),
    path('pages-login.html', views.login, name='pages-login'),
    path('index.html', views.index, name='index'),
    path('report-consumption.html', views.consumption, name='report-consumption'),
    path('report-failure.html', views.failure, name='report-failure'),
    path('report-integridy.html', views.integridy, name='report-integridy'),
    path('report-production.html', views.production, name='report-production'),
    # path('projecao_produtiva/', views.projecao_produtiva, name='projecao_produtiva'),
]