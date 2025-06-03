
from datetime import timedelta, timezone
from venv import logger
from rest_framework import generics,permissions, status
from rest_framework.response import Response

from payments.models import Payment
from .serializers import PaymentSerializer
from rest_framework.exceptions import ValidationError


class PaymentViewSet(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Payment created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({
                "status": status.HTTP_400_BAD_REQUES,
                "message": "Validation failed",
                "data": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)


