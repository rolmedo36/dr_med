from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Menu, MenuOpciones, Consultorios, Medicos, Clientes, CodigoPostal, Citas, Turnos, Turnos_agenda

# Register your models here.
admin.site.register(Menu)
admin.site.register(MenuOpciones)
admin.site.register(Consultorios)
admin.site.register(Medicos)
admin.site.register(Clientes)
admin.site.register(CodigoPostal)
admin.site.register(Citas)
admin.site.register(Turnos)
admin.site.register(Turnos_agenda)
