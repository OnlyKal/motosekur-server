import os
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics

from moto_sekur import settings

from .models import Motard, Video
from .serializers import IDcardImageUploadSerializer, MotardSerializer, MotardValidationSerializer, ProfileImageUploadSerializer, VideoSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from funcs.base64 import SendMail


import logging
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Montant, Moto, Payment
from .serializers import ImageMotoUploadSerializer, MontantSerializer, MotoSerializer, PaymentSerializer
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts import serializers





class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username, password = request.data.get('username'), request.data.get('password')
        if not username or not password:
            return Response({'message': 'Nom d’utilisateur et mot de passe requis.', 'status': 400}, status=400)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'message': 'Nom d’utilisateur ou mot de passe invalide.', 'status': 401}, status=401)
        if not user.is_active:
            return Response({'message': 'Ce compte est désactivé.', 'status': 403}, status=403)
        token = AccessToken.for_user(user)
        data = MotardSerializer(user).data
        return Response({'message': 'Connexion réussie.', 'status': status.HTTP_200_OK, 'token': 'Bearer ' + str(token), 'data': data})


class RegisterView(APIView):  
    permission_classes = [AllowAny]
    def post(self, request):
        s = MotardSerializer(data=request.data)
        if s.is_valid():
            u = s.save()
            token = AccessToken.for_user(u)
            return Response({
                'message': 'Compte créé.',
                'status': status.HTTP_200_OK,
                'data': s.data,
                'token': 'Bearer ' + str(token),
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Erreur de validation.',
            'status': 400,
            'data': s.errors
        }, status=400)




class MotardListView(generics.ListAPIView):
    serializer_class = MotardSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Motard.objects.filter(type_user='motard')


class MotardDetailView(generics.RetrieveAPIView):
    queryset = Motard.objects.all()
    serializer_class = MotardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class MotardUpdateView(generics.UpdateAPIView):
    queryset = Motard.objects.all()
    serializer_class = MotardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "message": "Motard mis à jour avec succès.",
            "status": status.HTTP_200_OK,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class MotardDeleteView(generics.DestroyAPIView):
    queryset = Motard.objects.all()
    serializer_class = MotardSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Motard supprimé avec succès."},
            status=status.HTTP_200_OK
        )

class MotardUpdateValidationView(generics.UpdateAPIView):
    queryset = Motard.objects.all()
    serializer_class = MotardValidationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        motard = self.get_object()
        serializer = self.get_serializer(motard, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            is_validated = request.data.get("is_validated")

            # Construction dynamique du sujet et du message
            subject = "VALIDATION DU COMPTE" if is_validated else "DÉSACTIVATION DU COMPTE"
            status_message = "validé" if is_validated else "désactivé"

            full_name = f"{motard.prenom} {motard.nom}" if hasattr(motard, 'prenom') and hasattr(motard, 'nom') else "Monsieur/Madame"
            matricule = motard.matricule if hasattr(motard, 'matricule') else "XXXXXXXX"

            message = (
                    f"Bonjour Cher(e) {full_name}, matricule {matricule},\n"
                    f"Nous vous informons que votre compte a été {status_message}. "
                )
            if is_validated:
                message += "Merci d’avoir participé à la formation.\n\n"
            else:
                message += "Nous vous recommandons de bien vouloir nous contacter pour connaître la cause.\n\n"
            message += "Cordialement,\nL’équipe MOTOSEKUR | BITA XPRESS | NEPA-RDC"
            message += "\n\n +(243) 855576225 | +(243) 999473877"


            SendMail.send(
                subject=subject,
                message=message,
                recipient_list=[motard.email]
            )

            return Response({'message': 'Validation réussie.', 'status': 200})
        
        return Response({'message': 'Échec de la validation.', 'errors': serializer.errors, 'status': 400}, status=400)


class ProfileImageUploadView(generics.UpdateAPIView):
    serializer_class = ProfileImageUploadSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class IDcardImageUploadView(generics.UpdateAPIView):
    serializer_class = IDcardImageUploadSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class OtherImageUploadView(generics.UpdateAPIView):
    serializer_class = IDcardImageUploadSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
    


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
    
class GetMotosByOwnerView(generics.GenericAPIView):
    serializer_class = MotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request): 
        motos = Moto.objects.filter(owner=request.user)
        serializer = self.get_serializer(motos, many=True)
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



class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        d= Video.objects.all().order_by('-date_creation')
        print("Queryset:", d)  # debug
        return d

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
     
        if not queryset.exists():
            return Response({
                "status": "error",
                "data": [],
                "message": "Aucune vidéo trouvée."
            }, status=404)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        })



# GET one video by ID
class VideoDetailView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    permission_classes = [permissions.AllowAny]  

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Http404:
            return Response({
                "status": "error",
                "data": None,
                "message": "Vidéo non trouvée."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
