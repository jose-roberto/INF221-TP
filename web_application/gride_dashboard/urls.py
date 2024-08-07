from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('projecao_produtiva/', views.projecao_produtiva, name='projecao_produtiva'),]