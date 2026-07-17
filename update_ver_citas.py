import os

base_template = 'E:/Proyectos Next/Zumedical/sistema_prenatal/paciente_general/templates/paciente_general/dashboard.html'
targets = ['E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/ver_citas.html']

with open(base_template, 'r', encoding='utf-8') as f:
    base_html = f.read()

base_top = base_html[:base_html.find('<!-- MAIN -->') + len('<!-- MAIN -->\n<main class="main">\n')]

base_top = base_top.replace('class="nav-item active"', 'class="nav-item"')
base_top = base_top.replace('href="{% url \'paciente_dashboard\' %}" class="nav-item"', 'href="{% url \'paciente_dashboard\' %}" class="nav-item active"')

for t in targets:
    if os.path.exists(t):
        with open(t, 'r', encoding='utf-8') as f:
            t_html = f.read()
        style_idx = t_html.rfind('</style>')
        if style_idx != -1:
            main_css_idx = t_html.find('/* Contenido principal */')
            if main_css_idx == -1:
                 main_css_idx = max(0, style_idx - 3000)
            css_to_keep = t_html[main_css_idx:style_idx]
        else:
            css_to_keep = ''

        main_start = t_html.find('<main class="main">') + len('<main class="main">')
        main_end = t_html.find('</main>')
        main_content = t_html[main_start:main_end]

        new_top = base_top.replace('</style>', css_to_keep + '\n</style>')
        new_html = new_top + '\n' + main_content + '\n</main>\n' + base_html[base_html.find('<script>'):]
        
        with open(t, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'Updated {t}')
