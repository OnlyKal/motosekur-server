from django.urls import path
from .views import (
     GetPaymentsByMatriculeView,
     PaymentViewSet
)

urlpatterns = [
    path('verification/', PaymentViewSet.as_view(), name='verification-payment'),
    path('get/<str:motard_matricule>/', GetPaymentsByMatriculeView.as_view(), name='payments-by-matricule'),
]

