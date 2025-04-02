from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Role

User = get_user_model()

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """Interface d'administration des rôles"""
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Interface d'administration des utilisateurs"""
    list_display = ('username', 'email', 'full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'preferred_district')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('username', 'email', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'phone_number', 'address')
        }),
        ('Préférences', {
            'fields': ('role', 'preferred_district', 'receive_alerts')
        }),
        ('Statut', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates importantes', {
            'fields': ('date_joined', 'last_login')
        }),
    )
    
    def full_name(self, obj):
        return obj.get_full_name()
    full_name.short_description = 'Nom complet'