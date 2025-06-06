# """
# URL configuration for moto_sekur project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static #add this
# from django.conf.urls.i18n import i18n_patterns

# app_name = "moto_sekur"
# urlpatterns = [
#     path('api/', include('api.urls')),
#     path('', admin.site.urls),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += i18n_patterns(prefix_default_language=False)

# admin.site.site_header = 'MOTOSEKUR'
# admin.site.site_title = 'MOTOSEKUR'

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

admin.site.site_header = 'MOTOSEKUR'
admin.site.site_title = 'MOTOSEKUR'

urlpatterns = [
    path('api/', include('api.urls')),
]

urlpatterns += i18n_patterns(
    path('', admin.site.urls),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
