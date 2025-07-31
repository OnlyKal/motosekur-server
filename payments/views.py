
from datetime import timedelta, timezone
import logging
from sqlite3 import IntegrityError
from venv import logger
from rest_framework import generics,permissions, status
from rest_framework.response import Response

from payments.models import Montant, Payment
from .serializers import MontantSerializer, PaymentSerializer
from rest_framework.exceptions import ValidationError

ogger = logging.getLogger(__name__)  # Optionnel : utile pour journaliser les erreurs

class PaymentViewSet(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)

            return Response({
                "status": "success",
                "message": "Paiement enregistré avec succès.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.warning(f"ValidationError: {e.detail}")  # Optionnel
            return Response({
                "status": "error",
                "message": "Erreur de validation.",
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as e:
            logger.error(f"IntegrityError: {str(e)}")  # Optionnel
            return Response({
                "status": "error",
                "message": "Une transaction avec cet identifiant existe déjà.",
                "errors": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unexpected error in Payment creation.")  # Optionnel
            return Response({
                "status": "error",
                "message": "Une erreur inattendue s'est produite.",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPaymentsByMatriculeView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        motard_matricule = self.kwargs.get('motard_matricule')
        return Payment.objects.filter(motard_matricule=motard_matricule)


class MontantListAPIView(generics.ListAPIView):
    queryset = Montant.objects.all()
    serializer_class = MontantSerializer
    permission_classes = [permissions.AllowAny]  