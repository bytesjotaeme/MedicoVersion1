# config/urls.py
from django.contrib import admin
from django.urls import path, include
# AÑADE ESTAS DOS LÍNEAS NUEVAS AL PRINCIPIO
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pacientes.urls')),
]

# AÑADE ESTE BLOQUE COMPLETO AL FINAL DEL ARCHIVO
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Sirve archivos multimedia solo durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)