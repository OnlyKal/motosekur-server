
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import datetime
import random
import string

from .models import Motard  # ici, l'import est OK car apps est prêt à ce moment

@receiver(pre_save, sender=Motard)
def generate_matricule(sender, instance, **kwargs):
    if not instance.matricule:
        today_str = datetime.now().strftime("%y%m%d")
        random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        username_prefix = instance.username[:3].upper() if instance.username else 'USR'
        instance.matricule = f"MOTOSEKUR{today_str}-{random_code}-{username_prefix}"
