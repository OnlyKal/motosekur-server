from django.urls import path
from .views import (
     PaymentViewSet
)

urlpatterns = [
    path('verification/', PaymentViewSet.as_view(), name='verification-payment')
]

