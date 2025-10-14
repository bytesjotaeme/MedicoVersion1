# pacientes/forms.py
from django import forms
from .models import Paciente, Turno, Antecedente, ExploracionFisica, Consulta, Doctor, Servicio, Horario # <-- Importa Horario

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['dni', 'nombre', 'apellido', 'email', 'telefono', 'fecha_nacimiento', 'sexo', 'domicilio', 'ciudad', 'observaciones']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['nombre', 'apellido', 'especialidad', 'telefono']

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'duracion_minutos', 'precio']

# --- AÑADE ESTE NUEVO FORMULARIO ---
class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['dia_semana', 'hora_inicio', 'hora_fin']
        widgets = {
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time'}),
        }
# --- FIN DEL NUEVO FORMULARIO ---

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['paciente', 'doctor', 'servicio', 'fecha', 'hora', 'motivo_consulta', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

class AntecedenteForm(forms.ModelForm):
    class Meta:
        model = Antecedente
        fields = ['personales', 'familiares', 'quirurgicos', 'alergias', 'medicamentos']
        widgets = {
            'personales': forms.Textarea(attrs={'rows': 4}),
            'familiares': forms.Textarea(attrs={'rows': 4}),
            'quirurgicos': forms.Textarea(attrs={'rows': 4}),
            'alergias': forms.Textarea(attrs={'rows': 4}),
            'medicamentos': forms.Textarea(attrs={'rows': 4}),
        }

class ExploracionFisicaForm(forms.ModelForm):
    class Meta:
        model = ExploracionFisica
        fields = ['peso', 'talla', 'presion_arterial', 'frecuencia_cardiaca', 'frecuencia_respiratoria', 'temperatura', 'hallazgos']
        widgets = {
            'hallazgos': forms.Textarea(attrs={'rows': 5}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['sintomas', 'diagnostico', 'tratamiento']
        widgets = {
            'sintomas': forms.Textarea(attrs={'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'rows': 4}),
            'tratamiento': forms.Textarea(attrs={'rows': 4}),
        }