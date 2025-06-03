
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Moto
from .serializers import ImageMotoUploadSerializer, MotoSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddMotoView(generics.CreateAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid()
        status_code = status.HTTP_201_CREATED if is_valid else status.HTTP_400_BAD_REQUEST

        if is_valid:
            serializer.save(owner=request.user)

        return Response({
            "status":  status.HTTP_200_OK,
            "message": "Moto ajoutée avec succès." if is_valid else "Erreur lors de l'ajout de la moto.",
            "data": serializer.data if is_valid else serializer.errors
        }, status=status_code)

class ListUserMotosView(generics.ListAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Moto.objects.filter(owner=self.request.user)

class GetMotoByIdView(generics.RetrieveAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Moto.objects.filter(owner=self.request.user)

class GetMotoByPlateView(generics.GenericAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, plate_number):
        moto = get_object_or_404(Moto, plate_number=plate_number, owner=request.user)
        serializer = self.get_serializer(moto)
        return Response(serializer.data)

class UpdateMotoView(generics.UpdateAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Moto.objects.filter(owner=self.request.user)
    


class DeleteMotoView(generics.DestroyAPIView):
    serializer_class = MotoSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Moto.objects.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": "Moto supprimée avec succès.",
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)
        
        
class ImageMotoUploadView(generics.UpdateAPIView):
    queryset = Moto.objects.all()
    serializer_class = ImageMotoUploadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'