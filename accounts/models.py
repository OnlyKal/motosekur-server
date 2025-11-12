from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe




class Motard(AbstractUser):
    matricule = models.CharField("Matricule", max_length=200 , unique=True, editable=True, blank=True)
    nom = models.CharField("Nom", max_length=150)
    prenom = models.CharField("Prénom", max_length=150)
    date_naissance = models.DateField("Date de naissance", null=True, blank=True)
    lieu_naissance = models.CharField("Lieu de naissance", max_length=255, null=True, blank=True)
    phone = models.CharField("Numéro de téléphone", max_length=20)
    email = models.CharField("Adresse Email", max_length=20)
    address = models.TextField("Adresse")
    photo_identite = models.ImageField("Photo d'identité récente", upload_to='photos_identite/%Y/', null=True, blank=True)
    autre_piece = models.ImageField("Autre pièce", upload_to='pieces_identite/%Y/', null=True, blank=True)
    profile = models.ImageField("Photo de profil", upload_to='profiles/%Y/', null=True, blank=True)
    is_validated = models.BooleanField("Compte validé", default=False)
    TYPE_USER_CHOICES = (
        ('motard', 'Motard'),
        ('motosekur', 'Moto Sekur'),
        ('autre', 'Autre'),
    )
    type_user = models.CharField("Type d'utilisateur", max_length=20, choices=TYPE_USER_CHOICES, default='motard')

    
    def _profile(self):
        if self.profile:
            return mark_safe('<div style="width: 65px; height: 65px; border: 1px solid #B5C0D0; border-radius: 10px; background-image: url({}); background-size: cover;backgroun-repeat:no-repeat;"></div>'.format(self.profile.url))
        else:
            return '(no picture)'
    
    _profile.short_description = 'profile Image'
    _profile.allow_tags = True
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
    # verbose_name = "Utilisateurs"
    # verbose_name_plural = "Liste des utilisateurs"

class UserProfile(models.Model):
    user = models.OneToOneField(Motard, on_delete=models.CASCADE, verbose_name="Utilisateur")

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.nom} {self.user.prenom}"



User = get_user_model()

class Moto(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='motos', verbose_name="Propriétaire")
    image = models.ImageField(upload_to='motos/%Y/', verbose_name="Photo de la moto", null=True, blank=True)
    brand = models.CharField(max_length=100, verbose_name="Marque")
    model = models.CharField(max_length=100, verbose_name="Modèle")
    plate_number = models.CharField(max_length=50, unique=True, verbose_name="Numéro de plaque")
    chassis_number = models.CharField(max_length=100, unique=True, verbose_name="Numéro de châssis")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'enregistrement")
    
    
    class Meta:
        verbose_name = "Moto"
        verbose_name_plural = "Motos Identifiées"

    def __str__(self):
        return f"{self.brand} - {self.plate_number}"
   
    def _image(self):
        if self.image:
            return mark_safe('<div style="width: 100px; height: 100px; border: 1px solid #B5C0D0; border-radius: 10px; background-image: url({}); background-size: cover;backgroun-repeat:no-repeat;"></div>'.format(self.image.url))
        else:
            return '(no picture)'
    
    _image.short_description = 'Moto Image'
    _image.allow_tags = True
  
  

class Video(models.Model):
    titre = models.CharField(max_length=255)
    categorie = models.CharField(max_length=100, default="Education")
    cover_image = models.ImageField(upload_to='videos/covers/')
    video = models.FileField(upload_to='videos/files/')
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre

    def _cover_image(self):
        if self.cover_image:
            return mark_safe(
                '<div style="width:95px; height:65px; border:1px solid #B5C0D0; '
                'border-radius:10px; background-image:url({}); background-size:cover; background-repeat:no-repeat;"></div>'.format(self.cover_image.url)
            )
        return '(no picture)'
    
    _cover_image.short_description = 'Cover Image Video'
    
    
class Montant(models.Model):
    montant_usd = models.CharField(
        max_length=100,
        verbose_name="Montant en USD",
        null=True,
        blank=True
    )
    montant_cdf = models.CharField(
        max_length=100,
        verbose_name="Montant en CDF",
        null=True,
        blank=True
    )
    actif = models.BooleanField(
        default=False,
        verbose_name="Montant Actif"
    )
    def __str__(self):
        return f"{self.montant_usd} {'(Actif)' if self.actif else ''}"

    class Meta:
        verbose_name = "Montant"
        verbose_name_plural = "Montants"
        
        
User = get_user_model()
class Payment(models.Model):
    TRANSACTION_STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('card', 'Carte'),
        ('mobile', 'Mobile Money'),
        ('bank', 'Virement Bancaire'),
        ('cash', 'Paiement Cash')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    motard_matricule=models.CharField(max_length=100, unique=True, verbose_name="ID Motard",null=True)
    transaction_id = models.CharField(max_length=100, unique=True, verbose_name="Identifiant de transaction")
    payment_status = models.CharField(max_length=20, choices=TRANSACTION_STATUS_CHOICES, verbose_name="Statut du paiement")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant payé")
    currency = models.CharField(max_length=10, default='USD', verbose_name="Devise")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Date de paiement")
    payer_name = models.CharField(max_length=255, verbose_name="Nom du payeur")
    payer_account = models.CharField(max_length=100, verbose_name="Compte/ID du payeur")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Méthode de paiement")
    bank_reference = models.CharField(max_length=100, blank=True, null=True, verbose_name="Référence bancaire")
    confirmation_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Code de confirmation")
    order_id = models.CharField(max_length=100,null=True, verbose_name="Identifiant de commande")
    fee = models.DecimalField(max_digits=12,null=True, decimal_places=2, default=0, verbose_name="Frais appliqués")
    signature = models.CharField(max_length=255,null=True, verbose_name="Signature numérique")
    notes = models.TextField(blank=True, null=True, verbose_name="Remarques")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.payment_status}"
    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Transaction de Formation"
        

