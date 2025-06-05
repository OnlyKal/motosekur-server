from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Motard

@admin.register(Motard)
class MotardAdmin(UserAdmin):
    model = Motard
    list_display = ("_profile",'matricule', 'nom', 'prenom', 'username', 'email', 'phone','type_user' ,'is_validated', 'is_staff', 'is_active')
    list_filter = ('is_validated', 'is_staff', 'is_active')
    search_fields = ('nom', 'prenom', 'username', 'email', 'phone')
    ordering = ('nom', 'prenom')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('matricule','nom', 'prenom', 'date_naissance', 'lieu_naissance', 'email', 'phone','type_user', 'address', 'photo_identite', 'autre_piece', 'profile')
        }),
        ('Permissions', {'fields': ('is_validated', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
