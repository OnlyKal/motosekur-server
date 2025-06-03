from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Motard

@admin.register(Motard)
class MotardAdmin(UserAdmin):
    model = Motard
    list_display = ("_profile", 'nom', 'prenom', 'username', 'email', 'phone', 'is_validated', 'is_staff', 'is_active')
    list_filter = ('is_validated', 'is_staff', 'is_active')
    search_fields = ('nom', 'prenom', 'username', 'email', 'phone')
    ordering = ('nom', 'prenom')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('nom', 'prenom', 'date_naissance', 'lieu_naissance', 'email', 'phone', 'address', 'photo_identite', 'autre_piece', 'profile')
        }),
        ('Permissions', {'fields': ('is_validated', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
