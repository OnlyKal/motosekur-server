from django.contrib.auth.models import AbstractUser
from django.db import models
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
    # type_user=()
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

class UserProfile(models.Model):
    user = models.OneToOneField(Motard, on_delete=models.CASCADE, verbose_name="Utilisateur")

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def __str__(self):
        return f"Profil de {self.user.nom} {self.user.prenom}"
