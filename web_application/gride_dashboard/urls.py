from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report-consumption', views.consumption, name='report-consumption'),
    path('report-failure.html', views.failure, name='report-failure'),
    path('report-integridy.html', views.integridy, name='report-integridy'),
    path('report-production.html', views.production, name='report-production'),
    # path('projecao_produtiva/', views.projecao_produtiva, name='projecao_produtiva'),
]