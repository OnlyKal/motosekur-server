from django.urls import path, include

urlpatterns = [
    path('auth/', include('accounts.urls')),
    path('moto/', include('motos.urls')),
    path('payment/', include('payments.urls')),
    # path('card/', include('cards.urls')),
    # path('formation/', include('trainings.urls')),
    # path('status/', include('permissions.urls')),
    # path('verify/', include('cards.urls')),  
]