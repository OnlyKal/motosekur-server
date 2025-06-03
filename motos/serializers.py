from rest_framework import serializers

from funcs.base64 import Base64ImageField
from .models import Moto, User

class MotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moto
        fields = '__all__'
        read_only_fields = ['owner', 'created_at']
        
class ImageMotoUploadSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    class Meta:
        model = User
        fields = ['image']