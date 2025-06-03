from django.contrib import admin
from .models import Moto

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('_image','owner', 'brand', 'model', 'plate_number', 'chassis_number', 'created_at')
    search_fields = ('brand', 'model', 'plate_number', 'chassis_number')
    list_filter = ('brand', 'created_at')
    ordering = ('-created_at',)
