# pacientes/models.py
from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    dni = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    domicilio = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.nombre} {self.apellido} ({self.especialidad})"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.duracion_minutos} min)"

class Turno(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('COMPLETADO', 'Completado'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    motivo_consulta = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')

    def __str__(self):
        return f"Turno para {self.paciente} con {self.doctor} el {self.fecha} a las {self.hora}"

class Antecedente(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, primary_key=True)
    personales = models.TextField(blank=True, null=True, help_text="Antecedentes médicos personales")
    familiares = models.TextField(blank=True, null=True, help_text="Antecedentes médicos familiares")
    quirurgicos = models.TextField(blank=True, null=True, help_text="Cirugías previas")
    alergias = models.TextField(blank=True, null=True)
    medicamentos = models.TextField(blank=True, null=True, help_text="Medicamentos que toma actualmente")

    def __str__(self):
        return f"Antecedentes de {self.paciente.nombre} {self.paciente.apellido}"

class ExploracionFisica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, primary_key=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso en kg")
    talla = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Talla en metros")
    presion_arterial = models.CharField(max_length=20, blank=True, null=True, help_text="Ej: 120/80")
    frecuencia_cardiaca = models.PositiveIntegerField(blank=True, null=True, help_text="Pulsaciones por minuto")
    frecuencia_respiratoria = models.PositiveIntegerField(blank=True, null=True, help_text="Respiraciones por minuto")
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="Temperatura en °C")
    hallazgos = models.TextField(blank=True, null=True, help_text="Hallazgos relevantes en la exploración")

    def __str__(self):
        return f"Exploración Física de {self.paciente.nombre} {self.paciente.apellido}"

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consultas')
    fecha_consulta = models.DateTimeField(default=timezone.now)
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    
    class Meta:
        ordering = ['-fecha_consulta']

    def __str__(self):
        return f"Consulta de {self.paciente.nombre} el {self.fecha_consulta.strftime('%d/%m/%Y')}"

# --- AÑADE ESTE NUEVO MODELO COMPLETO ---
class Horario(models.Model):
    DIA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    # Un doctor puede tener varios horarios. Si se borra el doctor, se borran sus horarios.
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIA_CHOICES)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        # Evita que se pueda crear un horario duplicado para el mismo doctor en el mismo día y hora
        unique_together = ('doctor', 'dia_semana', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"Horario de {self.doctor.apellido}: {self.get_dia_semana_display()} de {self.hora_inicio} a {self.hora_fin}"