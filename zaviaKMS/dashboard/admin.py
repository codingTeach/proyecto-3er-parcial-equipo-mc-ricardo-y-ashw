from django.contrib import admin
from .models import UserApp,Report

class UserAppAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')  # Columnas que se mostrarán en la lista
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Campos por los que se puede buscar
    list_filter = ('is_active', 'is_staff', 'date_joined')  # Filtros disponibles en el panel de administración
    ordering = ('-date_joined',)  # Orden de los resultados (por fecha de registro)

admin.site.register(UserApp, UserAppAdmin)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('affected_product', 'priority', 'created_by', 'assigned_to', 'created_at', 'modified_at')
    list_filter = ('priority', 'tags', 'created_at')
    search_fields = ('affected_product', 'description')