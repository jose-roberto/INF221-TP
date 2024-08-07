# Generated by Django 5.0.7 on 2024-08-07 00:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(max_length=14)),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('senha', models.CharField(max_length=50)),
                ('localizacao', models.CharField(max_length=200)),
                ('telefone', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=11)),
                ('dados_relatorio', models.TextField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('usina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gride_dashboard.usina')),
            ],
        ),
        migrations.CreateModel(
            name='DadosIntegridade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('integridade_placa', models.FloatField()),
                ('eficiencia_placa', models.FloatField()),
                ('usina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gride_dashboard.usina')),
            ],
        ),
        migrations.CreateModel(
            name='DadosFalhas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('falha', models.TextField()),
                ('usina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gride_dashboard.usina')),
            ],
        ),
        migrations.CreateModel(
            name='DadosDesempenho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('producao_energetica', models.FloatField()),
                ('consumo_energetico', models.FloatField()),
                ('valor_kwh', models.FloatField()),
                ('lucro', models.FloatField()),
                ('prejuizo', models.FloatField()),
                ('margem', models.FloatField()),
                ('tempo_de_operacao', models.FloatField()),
                ('tempo_de_parada', models.FloatField()),
                ('usina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gride_dashboard.usina')),
            ],
        ),
    ]
