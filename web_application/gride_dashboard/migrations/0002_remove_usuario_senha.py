# Generated by Django 5.1 on 2024-08-26 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gride_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='senha',
        ),
    ]
