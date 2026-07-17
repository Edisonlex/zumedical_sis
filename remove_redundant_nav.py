import os
import re

templates = [
    'paciente_general/templates/paciente_general/dashboard.html',
    'templates/paciente/dashboard_paciente.html',
    'paciente_general/templates/paciente_general/agendar_cita.html',
    'paciente_general/templates/paciente_general/mis_citas.html',
    'paciente_general/templates/paciente_general/mi_perfil.html'
]

old_block = """        <a href="{% url 'paciente_general_perfil' %}" class="nav-item">
            <i class="fa-regular fa-user"></i> Mi perfil
        </a>
        
"""

base_dir = "E:/Proyectos Next/Zumedical/sistema_prenatal"

for t in templates:
    filepath = os.path.join(base_dir, t)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_block in content:
            content = content.replace(old_block, "")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Removed redundant nav-item from {t}")
        else:
            print(f"Could not find exact block in {t}")
    else:
        print(f"File not found: {filepath}")
