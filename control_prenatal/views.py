from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HistoriaClinica, ControlPrenatal
from .forms import HistoriaClinicaForm, ControlPrenatalForm
from django.conf import settings


@login_required
def lista_historias(request):
    """Muestra la lista de historias clínicas (para médicos y admin)."""
    if request.user.rol not in ['medico', 'admin']:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('home')
    
    historias = HistoriaClinica.objects.select_related('paciente', 'medico').all().order_by('-fecha_registro')
    return render(request, 'control_prenatal/lista_historias.html', {'historias': historias})


@login_required
def detalle_historia(request, historia_id):
    """Muestra el detalle de una historia clínica y sus controles prenatales."""
    historia = get_object_or_404(HistoriaClinica, id=historia_id)
    controles = historia.paciente.controles_paciente.all().order_by('-fecha')
    
    # Verificar permisos: médico, admin o la propia paciente
    if request.user.rol not in ['medico', 'admin'] and request.user != historia.paciente:
        messages.error(request, 'No tienes permisos para acceder a esta historia.')
        return redirect('home')
    
    return render(request, 'control_prenatal/detalle_historia.html', {
        'historia': historia,
        'controles': controles
    })


@login_required
def crear_historia(request):
    """Crea una nueva historia clínica obstétrica."""
    if request.user.rol not in ['medico', 'admin']:
        messages.error(request, 'No tienes permisos para crear historias.')
        return redirect('home')
    
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, medico=request.user)
        if form.is_valid():
            historia = form.save(commit=False)
            historia.medico = request.user
            historia.save()
            messages.success(request, 'Historia clínica creada exitosamente.')
            return redirect('detalle_historia', historia_id=historia.id)
    else:
        form = HistoriaClinicaForm(medico=request.user)
    
    return render(request, 'control_prenatal/form_historia.html', {'form': form, 'titulo': 'Nueva Historia Clínica'})


@login_required
def editar_historia(request, historia_id):
    """Edita una historia clínica existente."""
    historia = get_object_or_404(HistoriaClinica, id=historia_id)
    
    if request.user.rol not in ['medico', 'admin']:
        messages.error(request, 'No tienes permisos para editar esta historia.')
        return redirect('home')
    
    if request.method == 'POST':
        form = HistoriaClinicaForm(request.POST, instance=historia, medico=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Historia clínica actualizada exitosamente.')
            return redirect('detalle_historia', historia_id=historia.id)
    else:
        form = HistoriaClinicaForm(instance=historia, medico=request.user)
    
    return render(request, 'control_prenatal/form_historia.html', {'form': form, 'titulo': 'Editar Historia Clínica'})


@login_required
def crear_control(request, paciente_id=None):
    """Crea un nuevo control prenatal."""
    if request.user.rol not in ['medico', 'admin']:
        messages.error(request, 'No tienes permisos para crear controles.')
        return redirect('home')
    
    paciente = None
    if paciente_id:
        paciente = get_object_or_404(settings.AUTH_USER_MODEL, id=paciente_id, rol='paciente')
    
    if request.method == 'POST':
        form = ControlPrenatalForm(request.POST, medico=request.user)
        if form.is_valid():
            control = form.save(commit=False)
            control.medico = request.user
            control.save()
            messages.success(request, 'Control prenatal registrado exitosamente.')
            # Redirigir a la historia clínica del paciente
            try:
                historia = HistoriaClinica.objects.get(paciente=control.paciente)
                return redirect('detalle_historia', historia_id=historia.id)
            except HistoriaClinica.DoesNotExist:
                return redirect('lista_historias')
    else:
        initial = {'paciente': paciente} if paciente else {}
        form = ControlPrenatalForm(initial=initial, medico=request.user)
    
    return render(request, 'control_prenatal/form_control.html', {'form': form, 'titulo': 'Nuevo Control Prenatal', 'paciente': paciente})


@login_required
def editar_control(request, control_id):
    """Edita un control prenatal existente."""
    control = get_object_or_404(ControlPrenatal, id=control_id)
    
    if request.user.rol not in ['medico', 'admin']:
        messages.error(request, 'No tienes permisos para editar este control.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ControlPrenatalForm(request.POST, instance=control, medico=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Control prenatal actualizado exitosamente.')
            try:
                historia = HistoriaClinica.objects.get(paciente=control.paciente)
                return redirect('detalle_historia', historia_id=historia.id)
            except HistoriaClinica.DoesNotExist:
                return redirect('lista_historias')
    else:
        form = ControlPrenatalForm(instance=control, medico=request.user)
    
    return render(request, 'control_prenatal/form_control.html', {'form': form, 'titulo': 'Editar Control Prenatal'})


@login_required
def mi_historial(request):
    """Muestra el historial prenatal de la paciente logueada."""
    if request.user.rol != 'paciente':
        messages.error(request, 'Solo pacientes pueden ver su historial.')
        return redirect('home')
    
    try:
        historia = HistoriaClinica.objects.get(paciente=request.user)
        controles = request.user.controles_paciente.all().order_by('-fecha')
    except HistoriaClinica.DoesNotExist:
        historia = None
        controles = []
    
    return render(request, 'control_prenatal/mi_historial.html', {'historia': historia, 'controles': controles})

