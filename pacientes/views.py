# pacientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Paciente, Turno, Antecedente, ExploracionFisica, Consulta, Doctor, Servicio, Horario
from .forms import PacienteForm, TurnoForm, AntecedenteForm, ExploracionFisicaForm, ConsultaForm, DoctorForm, ServicioForm, HorarioForm
from django.db.models import Q
import datetime
from django.utils import timezone

# --- Vistas de Pacientes ---
def lista_pacientes(request):
    query = request.GET.get('q', '')
    if query:
        pacientes = Paciente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query)
        )
    else:
        pacientes = Paciente.objects.all()
    # AQUÍ ESTABA EL ERROR, YA ESTÁ CORREGIDO
    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes, 'query': query})

def detalle_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    consultas = paciente.consultas.all()
    return render(request, 'pacientes/detalle_paciente.html', {'paciente': paciente, 'consultas': consultas})

def crear_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/crear_paciente.html', {'form': form})

def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'pacientes/editar_paciente.html', {'form': form})

def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    paciente.delete()
    return redirect('lista_pacientes')

def editar_antecedentes(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    antecedente, created = Antecedente.objects.get_or_create(paciente=paciente)
    if request.method == 'POST':
        form = AntecedenteForm(request.POST, instance=antecedente)
        if form.is_valid():
            form.save()
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = AntecedenteForm(instance=antecedente)
    return render(request, 'pacientes/editar_antecedentes.html', {'form': form, 'paciente': paciente})

def editar_exploracion_fisica(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    exploracion, created = ExploracionFisica.objects.get_or_create(paciente=paciente)
    if request.method == 'POST':
        form = ExploracionFisicaForm(request.POST, instance=exploracion)
        if form.is_valid():
            form.save()
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = ExploracionFisicaForm(instance=exploracion)
    return render(request, 'pacientes/editar_exploracion_fisica.html', {'form': form, 'paciente': paciente})

def agregar_consulta(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = ConsultaForm()
    return render(request, 'pacientes/agregar_consulta.html', {'form': form, 'paciente': paciente})

def agenda_calendario(request):
    doctores = Doctor.objects.all()
    return render(request, 'pacientes/agenda_calendario.html', {'doctores': doctores})

def lista_turnos(request):
    query = request.GET.get('q', '')
    turnos_list = Turno.objects.all().order_by('-fecha', '-hora')
    if query:
        turnos_list = turnos_list.filter(
            Q(paciente__nombre__icontains=query) |
            Q(paciente__apellido__icontains=query) |
            Q(doctor__nombre__icontains=query) |
            Q(doctor__apellido__icontains=query)
        )
    stats = {
        'total': Turno.objects.count(),
        'confirmados': Turno.objects.filter(estado='CONFIRMADO').count(),
        'cancelados': Turno.objects.filter(estado='CANCELADO').count(),
        'completados': Turno.objects.filter(estado='COMPLETADO').count(),
        'pendientes': Turno.objects.filter(estado='PENDIENTE').count(),
    }
    context = {
        'turnos': turnos_list,
        'stats': stats,
        'query': query,
    }
    return render(request, 'pacientes/lista_turnos.html', context)

def crear_turno(request):
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agenda_calendario')
    else:
        form = TurnoForm()
    return render(request, 'pacientes/crear_turno.html', {'form': form})

def editar_turno(request, id):
    turno = get_object_or_404(Turno, id=id)
    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            return redirect('agenda_calendario')
    else:
        form = TurnoForm(instance=turno)
    return render(request, 'pacientes/editar_turno.html', {'form': form})

def eliminar_turno(request, id):
    turno = get_object_or_404(Turno, id=id)
    turno.delete()
    return redirect('agenda_calendario')

def turnos_api(request):
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        turnos = Turno.objects.filter(doctor_id=doctor_id)
    else:
        turnos = Turno.objects.all()
    eventos = []
    for turno in turnos:
        if turno.servicio:
            duracion = turno.servicio.duracion_minutos
        else:
            duracion = 30
        start_time = datetime.datetime.combine(turno.fecha, turno.hora)
        end_time = start_time + datetime.timedelta(minutes=duracion)
        eventos.append({
            'title': f"{turno.paciente.nombre[0]}. {turno.paciente.apellido}",
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'borderColor': '#0dcaf0',
            'extendedProps': {
                'doctor': str(turno.doctor),
                'servicio': str(turno.servicio),
                'paciente': str(turno.paciente)
            }
        })
    return JsonResponse(eventos, safe=False)

def lista_doctores(request):
    doctores = Doctor.objects.all()
    return render(request, 'pacientes/lista_doctores.html', {'doctores': doctores})

def detalle_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.doctor = doctor
            horario.save()
            return redirect('detalle_doctor', id=doctor.id)
    else:
        form = HorarioForm()
    horarios = doctor.horarios.all().order_by('dia_semana', 'hora_inicio')
    return render(request, 'pacientes/detalle_doctor.html', {'doctor': doctor, 'horarios': horarios, 'form': form})

def crear_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save()
            return redirect('detalle_doctor', id=doctor.id)
    else:
        form = DoctorForm()
    return render(request, 'pacientes/doctor_form.html', {'form': form})

def editar_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('lista_doctores')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'pacientes/doctor_form.html', {'form': form, 'doctor': doctor})

def eliminar_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('lista_doctores')

def eliminar_horario(request, id):
    horario = get_object_or_404(Horario, id=id)
    doctor_id = horario.doctor.id
    if request.method == "POST":
        horario.delete()
        return redirect('detalle_doctor', id=doctor_id)
    return redirect('detalle_doctor', id=doctor_id)

def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'pacientes/lista_servicios.html', {'servicios': servicios})

def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm()
    return render(request, 'pacientes/servicio_form.html', {'form': form})

def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'pacientes/servicio_form.html', {'form': form, 'servicio': servicio})

def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect('lista_servicios')

def disponibilidad_api(request):
    doctor_id = request.GET.get('doctor_id')
    servicio_id = request.GET.get('servicio_id')
    fecha_str = request.GET.get('fecha')
    if not all([doctor_id, servicio_id, fecha_str]):
        return JsonResponse({'error': 'Faltan parámetros'}, status=400)
    try:
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        doctor = Doctor.objects.get(id=doctor_id)
        servicio = Servicio.objects.get(id=servicio_id)
    except (ValueError, Doctor.DoesNotExist, Servicio.DoesNotExist):
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)
    dia_semana = fecha.weekday()
    horarios_trabajo = Horario.objects.filter(doctor=doctor, dia_semana=dia_semana)
    turnos_reservados = Turno.objects.filter(doctor=doctor, fecha=fecha)
    slots_disponibles = []
    duracion_servicio = datetime.timedelta(minutes=servicio.duracion_minutos)
    for horario in horarios_trabajo:
        hora_actual = datetime.datetime.combine(fecha, horario.hora_inicio)
        hora_fin_trabajo = datetime.datetime.combine(fecha, horario.hora_fin)
        while hora_actual + duracion_servicio <= hora_fin_trabajo:
            esta_ocupado = False
            for turno in turnos_reservados:
                hora_inicio_turno = datetime.datetime.combine(turno.fecha, turno.hora)
                duracion_turno = datetime.timedelta(minutes=turno.servicio.duracion_minutos if turno.servicio else 30)
                hora_fin_turno = hora_inicio_turno + duracion_turno
                if max(hora_actual, hora_inicio_turno) < min(hora_actual + duracion_servicio, hora_fin_turno):
                    esta_ocupado = True
                    break
            if not esta_ocupado:
                slots_disponibles.append(hora_actual.strftime('%H:%M'))
            hora_actual += duracion_servicio
    return JsonResponse(slots_disponibles, safe=False)

def solicitar_turno(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        servicio_id = request.POST.get('servicio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        dni = request.POST.get('dni')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        paciente, created = Paciente.objects.get_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'email': email
            }
        )
        
        doctor = get_object_or_404(Doctor, id=doctor_id)
        servicio = get_object_or_404(Servicio, id=servicio_id)
        
        Turno.objects.create(
            paciente=paciente,
            doctor=doctor,
            servicio=servicio,
            fecha=fecha,
            hora=hora,
            estado='CONFIRMADO'
        )
        
        return redirect('solicitud_exitosa')

    doctores = Doctor.objects.all()
    servicios = Servicio.objects.all()
    context = {
        'doctores': doctores,
        'servicios': servicios,
    }
    return render(request, 'pacientes/solicitar_turno.html', context)

def solicitud_exitosa(request):
    return render(request, 'pacientes/solicitud_exitosa.html')