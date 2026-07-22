from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from citas.models import Cita
from control_prenatal.models import ControlPrenatal
from medicos.models import Medico
from landing.models import Especialidad

class RegistroPacienteForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name  = forms.CharField(max_length=100, label='Apellidos')
    cedula     = forms.CharField(max_length=10, label='Cédula')
    telefono   = forms.CharField(max_length=10, label='Teléfono')
    genero     = forms.ChoiceField(
        choices=[('', 'Selecciona tu género'), ('femenino', 'Femenino'), ('masculino', 'Masculino'), ('otro', 'Otro / Prefiero no indicar')],
        label='Género',
        required=True,
        help_text='Las pacientes femeninas pueden activar el módulo prenatal en el futuro',
    )

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cedula', 'telefono', 'genero', 'username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if Usuario.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está registrado. Elige otro.')
        return username

    def clean_cedula(self):
        from pacientes.models import Paciente
        cedula = self.cleaned_data.get('cedula', '').strip()
        if not cedula.isdigit() or len(cedula) != 10:
            raise forms.ValidationError('La cédula debe tener exactamente 10 dígitos numéricos.')
        if Paciente.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError('Esta cédula ya está registrada en el sistema.')
        return cedula

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if email and Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email


HORAS_CHOICES = [
    ('', 'Seleccione una hora'),
    ('08:30', '08:30 AM'), ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
    ('10:00', '10:00 AM'), ('10:30', '10:30 AM'), ('11:00', '11:00 AM'),
    ('11:30', '11:30 AM'), ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
    ('13:00', '01:00 PM'), ('13:30', '01:30 PM'),
    ('14:00', '02:00 PM'), ('14:30', '02:30 PM'), ('15:00', '03:00 PM'),
    ('15:30', '03:30 PM'), ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
    ('17:00', '05:00 PM'),
]


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.Select(choices=HORAS_CHOICES),
        }


class CitaEnfermeraForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['paciente', 'medico', 'fecha', 'hora', 'motivo']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.Select(choices=HORAS_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Usuario.objects.filter(rol='paciente')
        self.fields['medico'].queryset = Usuario.objects.filter(rol='medico')
        self.fields['paciente'].empty_label = "Seleccione un paciente"
        self.fields['medico'].empty_label = "Seleccione un médico"
        # Mostrar nombre completo en lugar del nombre de usuario
        self.fields['medico'].label_from_instance = lambda u: u.get_full_name() or u.username
        self.fields['paciente'].label_from_instance = lambda u: u.get_full_name() or u.username

class EditarPacienteEnfermeraForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name  = forms.CharField(max_length=100, label='Apellidos')
    cedula     = forms.CharField(max_length=10, label='Cédula')
    telefono   = forms.CharField(max_length=10, label='Teléfono')
    email      = forms.EmailField(label='Correo electrónico')
    username   = forms.CharField(max_length=150, label='Usuario')

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'cedula', 'telefono', 'username', 'email']

class PacienteBuscableSelect(forms.Select):
    """
    Select de paciente que agrega data-cedula a cada <option>,
    para permitir búsqueda por nombre o cédula en el frontend (JS).
    """
    def __init__(self, *args, cedulas=None, **kwargs):
        self.cedulas = cedulas or {}
        super().__init__(*args, **kwargs)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        val = getattr(value, 'value', value)
        if val:
            option['attrs']['data-cedula'] = self.cedulas.get(str(val), '')
        return option


def get_pacientes_con_acceso_prenatal():
    return Usuario.objects.filter(
        rol='paciente',
        paciente__estado_embarazo='ACTIVO'
    ).select_related('paciente').distinct().order_by('first_name', 'last_name', 'username')


class ControlPrenatalForm(forms.ModelForm):
    class Meta:
        model = ControlPrenatal
        fields = [
            'paciente',
            # Datos básicos
            'semanas_gestacion', 'presion_arterial', 'peso', 'altura',
            # Datos clínicos para IA
            'glucosa', 'frecuencia_cardiaca', 'temperatura',
            'embarazos_previos',
            'complicaciones_previas', 'diabetes_preexistente', 'diabetes_gestacional',
            # Score Mamá extra
            'proteinuria',
            # Historial clínico del control
            'examen_fisico', 'evolucion', 'resultado_examenes',
            'diagnostico', 'tratamiento', 'proxima_cita',
            # Observaciones
            'observaciones',
        ]
        widgets = {
            'semanas_gestacion':   forms.NumberInput(attrs={'placeholder': 'Ej: 20',  'min': 1,   'max': 42,  'step': 1}),
            'presion_arterial':    forms.TextInput(attrs={'placeholder': 'Ej: 120/80'}),
            'peso':                forms.NumberInput(attrs={'placeholder': 'Ej: 65.5', 'step': '0.1', 'min': 30, 'max': 200}),
            'altura':              forms.NumberInput(attrs={'placeholder': 'Ej: 1.62', 'step': '0.01','min': 1.2,'max': 2.2}),
            'glucosa':             forms.NumberInput(attrs={'placeholder': 'Ej: 90',   'step': '0.1', 'min': 40, 'max': 600}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'placeholder': 'Ej: 75',   'step': 1,    'min': 40, 'max': 200}),
            'temperatura':         forms.NumberInput(attrs={'placeholder': 'Ej: 98.0', 'step': '0.1','min': 95, 'max': 106}),
            'embarazos_previos':   forms.NumberInput(attrs={'placeholder': 'Ej: 0',    'step': 1,    'min': 0,  'max': 15}),
            'proteinuria':         forms.Select(choices=[('Negativa','Negativa'),('Trazas','Trazas'),('+1','+1'),('+2','+2'),('+3','+3')]),
            'examen_fisico':       forms.Textarea(attrs={'placeholder': 'Hallazgos del examen físico...', 'rows': 2}),
            'evolucion':           forms.Textarea(attrs={'placeholder': 'Evolución clínica desde el último control...', 'rows': 2}),
            'resultado_examenes':  forms.Textarea(attrs={'placeholder': 'Resultados de laboratorio, ecografías, etc.', 'rows': 2}),
            'diagnostico':         forms.Textarea(attrs={'placeholder': 'Diagnóstico(s) de este control...', 'rows': 2}),
            'tratamiento':         forms.Textarea(attrs={'placeholder': 'Tratamiento indicado...', 'rows': 2}),
            'proxima_cita':        forms.DateInput(attrs={'type': 'date'}),
            'observaciones':       forms.Textarea(attrs={'placeholder': 'Observaciones clínicas adicionales...', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from pacientes.models import Paciente
        qs = get_pacientes_con_acceso_prenatal()
        cedulas = {}
        for u in qs:
            try:
                cedulas[str(u.pk)] = u.paciente.cedula or ''
            except Paciente.DoesNotExist:
                cedulas[str(u.pk)] = ''
        self.fields['paciente'].widget = PacienteBuscableSelect(cedulas=cedulas)
        self.fields['paciente'].queryset = qs
        self.fields['paciente'].empty_label = "Seleccione una paciente"
        self.fields['paciente'].label_from_instance = lambda u: u.get_full_name() or u.username
        # Campos opcionales
        for field in ['examen_fisico', 'evolucion', 'resultado_examenes',
                      'diagnostico', 'tratamiento', 'proxima_cita']:
            self.fields[field].required = False


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        from control_prenatal.models import HistoriaClinica
        model = HistoriaClinica
        fields = [
            'paciente',
            # Antecedentes
            'antecedentes_personales', 'antecedentes_familiares', 'antecedentes_obstetricos',
            # Fórmula obstétrica
            'gestas', 'partos', 'cesareas', 'abortos', 'hijos_vivos',
            # Motivo
            'motivo_consulta',
            # Score Mamá
            'presion_arterial_inicial', 'frecuencia_cardiaca_inicial',
            'frecuencia_respiratoria', 'temperatura_inicial',
            'saturacion_oxigeno', 'estado_conciencia', 'proteinuria',
            # Antropometría
            'peso_inicial', 'talla',
            # Examen y diagnóstico
            'examen_fisico', 'evolucion_enfermedad', 'resultado_examenes',
            'diagnostico', 'tratamiento',
        ]
        widgets = {
            'antecedentes_personales':  forms.Textarea(attrs={'rows': 3, 'placeholder': 'Hipertensión, diabetes, cirugías previas, alergias...'}),
            'antecedentes_familiares':  forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enfermedades hereditarias, diabetes familiar, gemelos...'}),
            'antecedentes_obstetricos': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Partos anteriores, abortos, cesáreas, última regla...'}),
            'gestas':                   forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'partos':                   forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'cesareas':                 forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'abortos':                  forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'hijos_vivos':              forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'motivo_consulta':          forms.Textarea(attrs={'rows': 2, 'placeholder': 'Motivo principal de consulta...'}),
            'presion_arterial_inicial': forms.TextInput(attrs={'placeholder': 'Ej: 110/70'}),
            'frecuencia_cardiaca_inicial': forms.NumberInput(attrs={'min': 40, 'max': 200, 'placeholder': 'lpm'}),
            'frecuencia_respiratoria':  forms.NumberInput(attrs={'min': 8, 'max': 40, 'placeholder': 'rpm'}),
            'temperatura_inicial':      forms.NumberInput(attrs={'step': '0.1', 'min': 95, 'max': 106, 'placeholder': '°F'}),
            'saturacion_oxigeno':       forms.NumberInput(attrs={'min': 70, 'max': 100, 'placeholder': '%'}),
            'estado_conciencia':        forms.Select(choices=[('Alerta','Alerta'),('Somnoliento','Somnoliento'),('Confuso','Confuso'),('Inconsciente','Inconsciente')]),
            'proteinuria':              forms.Select(choices=[('Negativa','Negativa'),('Trazas','Trazas'),('+1','+1'),('+2','+2'),('+3','+3')]),
            'peso_inicial':             forms.NumberInput(attrs={'step': '0.1', 'min': 30, 'max': 200, 'placeholder': 'kg'}),
            'talla':                    forms.NumberInput(attrs={'step': '0.01', 'min': 1.2, 'max': 2.2, 'placeholder': 'm'}),
            'examen_fisico':            forms.Textarea(attrs={'rows': 3, 'placeholder': 'Hallazgos del examen físico general...'}),
            'evolucion_enfermedad':     forms.Textarea(attrs={'rows': 2, 'placeholder': 'Evolución de la enfermedad...'}),
            'resultado_examenes':       forms.Textarea(attrs={'rows': 2, 'placeholder': 'Resultados de laboratorio, ecografías...'}),
            'diagnostico':              forms.Textarea(attrs={'rows': 2, 'placeholder': 'Diagnóstico(s)...'}),
            'tratamiento':              forms.Textarea(attrs={'rows': 2, 'placeholder': 'Tratamiento indicado...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from pacientes.models import Paciente
        qs = get_pacientes_con_acceso_prenatal()
        cedulas = {}
        for u in qs:
            try:
                cedulas[str(u.pk)] = u.paciente.cedula or ''
            except Paciente.DoesNotExist:
                cedulas[str(u.pk)] = ''
        self.fields['paciente'].widget = PacienteBuscableSelect(cedulas=cedulas)
        self.fields['paciente'].queryset = qs
        self.fields['paciente'].empty_label = "Seleccione una paciente"
        self.fields['paciente'].label_from_instance = lambda u: u.get_full_name() or u.username
        # Todos los campos clínicos son opcionales
        for field in ['antecedentes_personales','antecedentes_familiares','antecedentes_obstetricos',
                      'motivo_consulta','presion_arterial_inicial','frecuencia_cardiaca_inicial',
                      'frecuencia_respiratoria','temperatura_inicial','saturacion_oxigeno',
                      'peso_inicial','talla','examen_fisico','evolucion_enfermedad',
                      'resultado_examenes','diagnostico','tratamiento']:
            self.fields[field].required = False

class MedicoForm(forms.ModelForm):
    """Formulario para crear/editar el perfil médico (especialidad, teléfono)."""
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.filter(activo=True),
        empty_label="— Selecciona una especialidad —",
        label="Especialidad",
        required=False
    )
    telefono = forms.CharField(max_length=10, label="Teléfono", required=False)

    class Meta:
        model = Medico
        fields = ['especialidad', 'telefono']


class AdminCrearMedicoForm(UserCreationForm):
    """Formulario completo para que el admin cree un médico."""
    first_name = forms.CharField(max_length=100, label='Nombre')
    last_name  = forms.CharField(max_length=100, label='Apellidos')
    email      = forms.EmailField(label='Correo electrónico', required=False)
    especialidad = forms.ModelChoiceField(
        queryset=Especialidad.objects.filter(activo=True),
        empty_label="— Selecciona una especialidad —",
        label="Especialidad",
        required=False
    )
    telefono = forms.CharField(max_length=10, label='Teléfono', required=False)

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
