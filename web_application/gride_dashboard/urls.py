from django.urls import path
from .views import *
from django.conf.urls import handler404
from django.shortcuts import render


def custom_404(request, exception):
    return render(request, '404.html', status=404)


urlpatterns = [
    path('', IndexView.as_view(), name='index'), #
    path('index/', IndexView.as_view(), name='index'), #
    path('homepage/', HomepageView.as_view(), name='homepage'),
    path('report-failure/', failureView, name='report-failure'),
    path('report-integridy/', integridyView, name='report-integridy'),
    path('report-production/', productionView, name='report-production'),
    path('projection/', projectionView, name='projection'),
    path('proxy-cache/', proxyView, name='proxy-cache'),
    path('pages-contact/', ContactView.as_view(), name='pages-contact'),
    
    path('users-profile/', read_user, name='profile'),
    path('read_user/', read_user, name='read_user'),
    path('update_user/', update_user, name='update_user'),    
    path('pages-register/', register, name='pages-register'), #
    path('pages-login/', login, name='pages-login'), #
    path('logout/', logout, name='logout'), #
    
    ## CRUD usado para testes, não na versão final

    # path('create/dados-integridade/', CreateDadosIntegridade.as_view(), name='create-dados-integridade'),
    # path('update/dados-integridade/<int:pk>/', UpdateDadosIntegridade.as_view(), name='update-dados-integridade'),
    # path('delete/dados-integridade/<int:pk>/', DeleteDadosIntegridade.as_view(), name='delete-dados-integridade'),
    # path('list/dados-integridade/', ListDadosIntegridade.as_view(), name='list-dados-integridade'),

    # path('create/dados-falhas/', CreateDadosFalhas.as_view(), name='create-dados-falhas'),
    # path('update/dados-falhas/<int:pk>/', UpdateDadosFalhas.as_view(), name='update-dados-falhas'),
    # path('delete/dados-falhas/<int:pk>/', DeleteDadosFalhas.as_view(), name='delete-dados-falhas'),
    # path('list/dados-falhas/', ListDadosFalhas.as_view(), name='list-dados-falhas'),

    # path('create/dados-desempenho/', CreateDadosDesempenho.as_view(), name='create-dados-desempenho'),
    # path('update/dados-desempenho/<int:pk>/', UpdateDadosDesempenho.as_view(), name='update-dados-desempenho'),
    # path('delete/dados-desempenho/<int:pk>/', DeleteDadosDesempenho.as_view(), name='delete-dados-desempenho'),
    # path('list/dados-desempenho/', ListDadosDesempenho.as_view(), name='list-dados-desempenho'),

    # path('create/cache-relatorio/', CreateCacheRelatorio.as_view(), name='create-cache-relatorio'),
    # path('update/cache-relatorio/<int:pk>/', UpdateCacheRelatorio.as_view(), name='update-cache-relatorio'),
    # path('delete/cache-relatorio/<int:pk>/', DeleteCacheRelatorio.as_view(), name='delete-cache-relatorio'),
    # path('list/cache-relatorio/', ListCacheRelatorio.as_view(), name='list-cache-relatorio'),
]


handler404 = custom_404