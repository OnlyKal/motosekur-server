from rest_framework import serializers
from funcs.base64 import Base64ImageField
from motos.models import User
from .models import Motard

class MotardSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(read_only=True)
    class Meta:
        model = Motard
        fields = [
            'id',
            'username',
            'email',
            'nom',
            'prenom',
            'date_naissance',
            'lieu_naissance',
            'phone',
            'address',
            'photo_identite',
            'autre_piece',
            'profile',  
            'is_validated',
        ]
        
class MotardValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motard
        fields = ['is_validated']
        
        
class ProfileImageUploadSerializer(serializers.ModelSerializer):
    profile = Base64ImageField(required=True)
    class Meta:
        model = User
        fields = ['profile']
        
class IDcardImageUploadSerializer(serializers.ModelSerializer):
    photo_identite = Base64ImageField(required=True)
    class Meta:
        model = User
        fields = ['photo_identite']
        
class OtherImageUploadSerializer(serializers.ModelSerializer):
    autre_piece = Base64ImageField(required=True)
    class Meta:
        model = User
        fields = ['autre_piece']