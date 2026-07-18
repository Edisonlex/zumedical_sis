import os
import re

views_path = r'E:\Proyectos Next\Zumedical\sistema_prenatal\usuarios\views.py'
with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

view_code = '''
@login_required
@no_cache_view
def cambiar_estado_cita(request, cita_id):
    if request.method == 'POST':
        cita = get_object_or_404(Cita, id=cita_id)
        
        # Validar permisos
        if request.user.rol not in ['medico', 'administrador', 'secretaria'] or (request.user.rol == 'medico' and cita.medico != request.user):
            messages.error(request, 'No tienes permiso para modificar esta cita.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
        nuevo_estado = request.POST.get('estado')
        estados_validos = dict(Cita.ESTADO).keys()
        
        if nuevo_estado in estados_validos:
            cita.estado = nuevo_estado
            cita.save()
            messages.success(request, f'Estado de la cita actualizado a {cita.get_estado_display()}.')
        else:
            messages.error(request, 'Estado seleccionado no es válido.')
            
    return redirect(request.META.get('HTTP_REFERER', 'citas_medico'))
'''

if 'def cambiar_estado_cita' not in content:
    with open(views_path, 'a', encoding='utf-8') as f:
        f.write('\n' + view_code + '\n')
    print('View added.')
else:
    print('View already exists.')

urls_path = r'E:\Proyectos Next\Zumedical\sistema_prenatal\usuarios\urls.py'
with open(urls_path, 'r', encoding='utf-8') as f:
    urls_content = f.read()

urls_content = re.sub(r"#\s*path\('cambiar-estado/<int:cita_id>/', views\.cambiar_estado_cita, name='cambiar_estado_cita'\).*", "path('cambiar-estado/<int:cita_id>/', views.cambiar_estado_cita, name='cambiar_estado_cita'),", urls_content)

with open(urls_path, 'w', encoding='utf-8') as f:
    f.write(urls_content)
print('URLs updated.')
