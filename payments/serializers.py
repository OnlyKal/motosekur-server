from rest_framework import serializers
from .models import Montant, Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        
class MontantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Montant
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('actif'):
            Montant.objects.filter(actif=True).update(actif=False)
        return super().validate(attrs)
