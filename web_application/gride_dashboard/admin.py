from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Usuario)
admin.site.register(DadosIntegridade)
admin.site.register(DadosFalha)
admin.site.register(DadosDesempenho)
admin.site.register(CacheRelatorio)
