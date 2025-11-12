from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Motard
from django.contrib import admin
from .models import Moto, Video
from django.http import HttpResponse
import openpyxl
from .models import Montant, Payment


@admin.register(Motard)
class MotardAdmin(UserAdmin):
    model = Motard
    list_display = ("_profile",'id','matricule', 'nom', 'prenom', 'username', 'email', 'phone','type_user' ,'is_validated', 'is_staff', 'is_active')
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

@admin.register(Moto)
class MotoAdmin(admin.ModelAdmin):
    list_display = ('_image','owner', 'brand', 'model', 'plate_number', 'chassis_number', 'created_at')
    search_fields = ('brand', 'model', 'plate_number', 'chassis_number')
    list_filter = ('brand', 'created_at')
    ordering = ('-created_at',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('_cover_image', 'titre', 'categorie', 'date_creation')
    search_fields = ('titre', 'categorie')
    list_filter = ('categorie', 'date_creation')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'motard_matricule', 'payment_status', 'amount', 'currency', 'payment_date', 'payer_name', 'payment_method', 'order_id')
    search_fields = ('transaction_id', 'payer_name', 'order_id')
    list_filter = ('payment_status', 'payment_method', 'currency')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['export_to_excel']

    @admin.action(description="Exporter les paiements sélectionnés en Excel")
    def export_to_excel(self, request, queryset):
        # Créer un classeur Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Payments"

        # Titres des colonnes
        headers = [
            'Transaction ID','Matricule' 'Statut', 'Montant', 'Devise', 'Date de Paiement',
            'Nom du Payeur', 'Compte du Payeur', 'Méthode de Paiement',
            'Référence Banque', 'Code Confirmation', 'Commande', 'Frais',
            'Signature', 'Notes', 'Créé le', 'Mis à jour'
        ]
        ws.append(headers)

        # Ajouter les lignes de données
        for p in queryset:
            ws.append([
                p.transaction_id,
                p.motard_matricule,
                p.payment_status,
                str(p.amount),
                p.currency,
                p.payment_date.strftime('%Y-%m-%d %H:%M'),
                p.payer_name,
                p.payer_account,
                p.payment_method,
                p.bank_reference,
                p.confirmation_code,
                p.order_id,
                str(p.fee),
                p.signature,
                p.notes,
                p.created_at.strftime('%Y-%m-%d %H:%M'),
                p.updated_at.strftime('%Y-%m-%d %H:%M'),
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename=paiments_export.xlsx'
        wb.save(response)
        return response
    
@admin.register(Montant)
class MontantAdmin(admin.ModelAdmin):
    list_display = ('id', 'montant_usd', 'montant_cdf', 'actif')