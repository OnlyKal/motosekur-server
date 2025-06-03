from django.db import models
from motos.models import User
from django.contrib.auth import get_user_model



User = get_user_model()
class Payment(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Carte'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement Bancaire'),
        ('cash', 'Paiement Cash'),
        # Ajoutez d'autres méthodes si besoin
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name="Identifiant de transaction")
    payment_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, verbose_name="Statut du paiement")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant payé")
    currency = models.CharField(max_length=10, default='XAF', verbose_name="Devise")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de paiement")
    payer_name = models.CharField(max_length=255, verbose_name="Nom du payeur")
    payer_account = models.CharField(max_length=100, verbose_name="Compte/ID du payeur")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Méthode de paiement")
    bank_reference = models.CharField(max_length=100, blank=True, null=True, verbose_name="Référence bancaire")
    confirmation_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Code de confirmation")
    order_id = models.CharField(max_length=100, verbose_name="Identifiant de commande")
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Frais appliqués")
    signature = models.CharField(max_length=255, verbose_name="Signature numérique")
    notes = models.TextField(blank=True, null=True, verbose_name="Remarques")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.payment_status}"
