# Generated by Django 5.0.7 on 2024-08-07 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gride_dashboard', '0002_rename_relatorio_relatorioconsumo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RelatorioProjecao',
            new_name='CacheRelatorioConsumo',
        ),
        migrations.RenameModel(
            old_name='RelatorioProducao',
            new_name='CacheRelatorioFalhas',
        ),
        migrations.RenameModel(
            old_name='RelatorioFalhas',
            new_name='CacheRelatorioIntegridade',
        ),
        migrations.RenameModel(
            old_name='RelatorioIntegridade',
            new_name='CacheRelatorioProducao',
        ),
        migrations.RenameModel(
            old_name='RelatorioConsumo',
            new_name='CacheRelatorioProjecao',
        ),
    ]
