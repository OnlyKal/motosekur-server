from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, generics

from motos.models import User
from .models import Motard
from .serializers import IDcardImageUploadSerializer, MotardSerializer, MotardValidationSerializer, ProfileImageUploadSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from funcs.base64 import SendMail

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



# READ — List all motards  GET
class MotardListView(generics.ListAPIView):
    serializer_class = MotardSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Motard.objects.filter(type_user='motard')

# READ — Retrieve single motard by ID GET
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