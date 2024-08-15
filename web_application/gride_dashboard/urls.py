from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('homepage.html', views.homepage, name='homepage'),
    path('pages-register.html', views.register, name='pages-register'),
    path('pages-login.html', views.login, name='pages-login'),
    path('logout', views.logout, name='logout'),
    path('report-consumption.html', views.consumption, name='report-consumption'),
    path('report-failure.html', views.failure, name='report-failure'),
    path('report-integridy.html', views.integridy, name='report-integridy'),
    path('report-production.html', views.production, name='report-production'),
    path('projection.html', views.projection, name='projection'),
    path('users-profile.html', views.profile, name='profile'),
    path('read_user', views.read_user, name='read_user'),
    path('update_user', views.update_user, name='update_user'),    
    path('pages-contact.html', views.contact, name='pages-contact'),    
    # path('projecao_produtiva/', views.projecao_produtiva, name='projecao_produtiva'),
]