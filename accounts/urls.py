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
    path('upload-idx/', OtherImageUploadView.as_view(), name='upload-idx')
]
