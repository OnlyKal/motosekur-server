from django.urls import path
from .views import (
    AddMotoView,
    ImageMotoUploadView,
    ListUserMotosView,
    GetMotoByIdView,
    GetMotoByPlateView,
    UpdateMotoView,
    DeleteMotoView
)


urlpatterns = [
    path('add/', AddMotoView.as_view(), name='add-moto'),
    path('all/', ListUserMotosView.as_view(), name='list-motos'),
    path('<int:pk>/', GetMotoByIdView.as_view(), name='get-moto-by-id'),
    path('plate/<str:plate_number>/', GetMotoByPlateView.as_view(), name='get-moto-by-plate'),
    path('update/<int:pk>/', UpdateMotoView.as_view(), name='update-moto'),
    path('remove/<int:id>/', DeleteMotoView.as_view(), name='remove-moto'),
    path('upload/<int:id>/', ImageMotoUploadView.as_view(), name='upload-moto-image')
]

