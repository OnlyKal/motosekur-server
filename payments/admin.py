from django.contrib import admin
from django.http import HttpResponse
import openpyxl
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'payment_status', 'amount', 'currency', 'payment_date', 'payer_name', 'payment_method', 'order_id')
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
            'Transaction ID', 'Statut', 'Montant', 'Devise', 'Date de Paiement',
            'Nom du Payeur', 'Compte du Payeur', 'Méthode de Paiement',
            'Référence Banque', 'Code Confirmation', 'Commande', 'Frais',
            'Signature', 'Notes', 'Créé le', 'Mis à jour'
        ]
        ws.append(headers)

        # Ajouter les lignes de données
        for p in queryset:
            ws.append([
                p.transaction_id,
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