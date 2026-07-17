import os

templates = [
    'agendar_cita.html',
    'mis_citas.html',
    'mi_perfil.html'
]

old_block = """        {% if request.user.puede_prenatal %}
        <a href="{% url 'paciente_dashboard' %}" class="nav-item">
            <i class="fa-solid fa-person-pregnant"></i> Módulo prenatal
        </a>
        {% endif %}"""

new_block = """        <a href="{% url 'paciente_general_perfil' %}" class="nav-item">
            <i class="fa-regular fa-user"></i> Mi perfil
        </a>
        
        {% if request.user.paciente.estado_embarazo == 'ACTIVO' %}
        <a href="{% url 'paciente_dashboard' %}" class="nav-item" style="margin-top: 1.5rem;">
            <i class="fa-solid fa-person-pregnant"></i> Mi embarazo
        </a>
        {% endif %}"""

base_dir = "E:/Proyectos Next/Zumedical/sistema_prenatal/paciente_general/templates/paciente_general"

for t in templates:
    filepath = os.path.join(base_dir, t)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_block in content:
        content = content.replace(old_block, new_block)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {t}")
    else:
        # Fallback if there are minor whitespace differences
        print(f"Could not find exact block in {t}")
