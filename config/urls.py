# config/urls.py
from django.contrib import admin
from django.urls import path, include  # <-- Asegúrate de que 'include' esté aquí

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pacientes.urls')), # <-- AÑADE ESTA LÍNEA
]