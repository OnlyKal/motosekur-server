from django.urls import path
from .views import (
    IDcardImageUploadView,
    LoginView,
    MotardUpdateValidationView,
    OtherImageUploadView,
    ProfileImageUploadView,
    RegisterView,
    MotardListView,
    MotardDetailView,
    MotardUpdateView,
    MotardDeleteView,
    AddMotoView,
    GetMotosByOwnerView,
    ImageMotoUploadView,
    ListUserMotosView,
    GetMotoByIdView,
    GetMotoByPlateView,
    UpdateMotoView,
    DeleteMotoView,
    GetPaymentsByMatriculeView,
    PaymentViewSet,MontantListAPIView,
    VideoDetailView,
    VideoListView
)


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='motard-register'),
    path('motards/', MotardListView.as_view(), name='motard-list'),
    path('motards/<int:id>/', MotardDetailView.as_view(), name='motard-detail'),
    path('motards/<int:id>/update/', MotardUpdateView.as_view(), name='motard-update'),
    path('motards/<int:id>/delete/', MotardDeleteView.as_view(), name='motard-delete'),
    path('motards/validate/<int:id>/', MotardUpdateValidationView.as_view(), name='motard-update-validate'),
    path('upload-profile/', ProfileImageUploadView.as_view(), name='upload-profile'),
    path('upload-id/', IDcardImageUploadView.as_view(), name='upload-id-card'),
    path('upload-idx/', OtherImageUploadView.as_view(), name='upload-idx'),

    path('moto/add/', AddMotoView.as_view(), name='add-moto'),
    path('moto/all/', ListUserMotosView.as_view(), name='list-motos'),
    path('moto/<int:pk>/', GetMotoByIdView.as_view(), name='get-moto-by-id'),
    path('moto/plate/<str:plate_number>/', GetMotoByPlateView.as_view(), name='get-moto-by-plate'),
    path('moto/update/<int:pk>/', UpdateMotoView.as_view(), name='update-moto'),
    path('moto/remove/<int:id>/', DeleteMotoView.as_view(), name='remove-moto'),
    path('moto/upload/<int:id>/', ImageMotoUploadView.as_view(), name='upload-moto-image'),
    path('moto/my/', GetMotosByOwnerView.as_view()),
    
    path('get-price/', MontantListAPIView.as_view(), name='price-payment'),
    path('p/verification/', PaymentViewSet.as_view(), name='verification-payment'),
    path('p/<str:motard_matricule>/', GetPaymentsByMatriculeView.as_view(), name='payments-by-matricule'),
    
    path('all/videos/', VideoListView.as_view(), name='video-list'),
    path('get/videos/<int:id>/', VideoDetailView.as_view(), name='video-detail'),

]


