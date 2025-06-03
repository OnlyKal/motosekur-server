from django.db import models
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

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
        verbose_name_plural = "Motos"

    def __str__(self):
        return f"{self.brand} - {self.plate_number}"
   
    def _image(self):
        if self.image:
            return mark_safe('<div style="width: 100px; height: 100px; border: 1px solid #B5C0D0; border-radius: 10px; background-image: url({}); background-size: cover;backgroun-repeat:no-repeat;"></div>'.format(self.image.url))
        else:
            return '(no picture)'
    
    _image.short_description = 'Moto Image'
    _image.allow_tags = True
  