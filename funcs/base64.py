import base64
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
            return super().to_internal_value(img_data)
        return super().to_internal_value(data)
    
class SendMail:
    @staticmethod
    def send(subject, message, recipient_list):
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False
        )