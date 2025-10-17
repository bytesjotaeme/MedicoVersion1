# pacientes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- NUEVAS RUTAS PÚBLICAS ---
    path('', views.homepage, name='homepage'),
    path('solicitar-turno/', views.solicitar_turno, name='solicitar_turno'),
    path('solicitud-exitosa/', views.solicitud_exitosa, name='solicitud_exitosa'),

    # --- RUTAS DEL PANEL DE ADMINISTRACIÓN ---
    path('dashboard/', views.lista_pacientes, name='lista_pacientes'),

    path('pacientes/<int:id>/', views.detalle_paciente, name='detalle_paciente'),
    path('pacientes/nuevo/', views.crear_paciente, name='crear_paciente'),
    path('pacientes/editar/<int:id>/', views.editar_paciente, name='editar_paciente'),
    path('pacientes/eliminar/<int:id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('pacientes/<int:id>/antecedentes/', views.editar_antecedentes, name='editar_antecedentes'),
    path('pacientes/<int:id>/exploracion/', views.editar_exploracion_fisica, name='editar_exploracion_fisica'),
    path('pacientes/<int:id>/consultas/nueva/', views.agregar_consulta, name='agregar_consulta'),
    path('pacientes/<int:id>/documentos/nuevo/', views.agregar_documento, name='agregar_documento'),

    path('agenda/', views.agenda_calendario, name='agenda_calendario'),
    path('turnos/', views.lista_turnos, name='lista_turnos'),
    path('turnos/nuevo/', views.crear_turno, name='crear_turno'),
    path('turnos/editar/<int:id>/', views.editar_turno, name='editar_turno'),
    path('turnos/eliminar/<int:id>/', views.eliminar_turno, name='eliminar_turno'),

    path('api/turnos/', views.turnos_api, name='turnos_api'),
    path('api/disponibilidad/', views.disponibilidad_api, name='disponibilidad_api'),

    path('doctores/', views.lista_doctores, name='lista_doctores'),
    path('doctores/<int:id>/', views.detalle_doctor, name='detalle_doctor'),
    path('doctores/nuevo/', views.crear_doctor, name='crear_doctor'),
    path('doctores/editar/<int:id>/', views.editar_doctor, name='editar_doctor'),
    path('doctores/eliminar/<int:id>/', views.eliminar_doctor, name='eliminar_doctor'),
    path('horarios/eliminar/<int:id>/', views.eliminar_horario, name='eliminar_horario'),

    path('servicios/', views.lista_servicios, name='lista_servicios'),
    path('servicios/nuevo/', views.crear_servicio, name='crear_servicio'),
    path('servicios/editar/<int:id>/', views.editar_servicio, name='editar_servicio'),
    path('servicios/eliminar/<int:id>/', views.eliminar_servicio, name='eliminar_servicio'),
]