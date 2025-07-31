from django.urls import path
from .views import (
     GetPaymentsByMatriculeView,
     PaymentViewSet,MontantListAPIView
)

urlpatterns = [
    path('price/', MontantListAPIView.as_view(), name='price-payment'),
    path('verification/', PaymentViewSet.as_view(), name='verification-payment'),
    path('get/<str:motard_matricule>/', GetPaymentsByMatriculeView.as_view(), name='payments-by-matricule'),
]

