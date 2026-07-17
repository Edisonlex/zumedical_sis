import os

base_template = 'E:/Proyectos Next/Zumedical/sistema_prenatal/paciente_general/templates/paciente_general/dashboard.html'

targets = [
    'E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/evaluar_riesgo.html',
    'E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/chatbot.html'
]

with open(base_template, 'r', encoding='utf-8') as f:
    base_html = f.read()

base_top = base_html[:base_html.find('<!-- MAIN -->') + len('<!-- MAIN -->\n<main class="main">\n')]
base_topbar = base_html[base_html.find('<!-- TOPBAR -->'):base_html.find('<!-- HERO BANNER -->')]

# We must ensure that active states for sidebars are correct. Wait, we want ONE sidebar. 
# If they are inside Mi embarazo, maybe we don't highlight any? Or just "Mi embarazo"?
# "Mi embarazo" should probably be active for evaluar_riesgo and chatbot since they belong to it.
base_top = base_top.replace('class="nav-item active"', 'class="nav-item"')
base_top = base_top.replace('href="{% url \'paciente_dashboard\' %}" class="nav-item"', 'href="{% url \'paciente_dashboard\' %}" class="nav-item active"')

for t in targets:
    if os.path.exists(t):
        with open(t, 'r', encoding='utf-8') as f:
            t_html = f.read()
            
        # extract CSS
        css_start = t_html.find('/* Aviso informativo */')
        if css_start == -1:
            css_start = t_html.find('/* Chatbot */')
        if css_start == -1:
            css_start = t_html.find('/* HEADER */')
        
        css_end = t_html.find('/* RESPONSIVE */')
        if css_end == -1:
            css_end = t_html.find('@media(max-width:')
        
        if css_start != -1 and css_end != -1:
            css_to_keep = t_html[css_start:css_end]
        else:
            # try finding from </style> backwards
            style_idx = t_html.rfind('</style>')
            # just take the last 2000 chars of style, assuming it's specific
            css_to_keep = t_html[max(0, style_idx-3000):style_idx]
            # remove common stuff, this might be risky. 
            # Better to just extract after "/* ── MAIN ── */" or similar.
            main_css_idx = t_html.find('/* Contenido principal */')
            if main_css_idx != -1:
                css_to_keep = t_html[main_css_idx:style_idx]

        # extract main content
        main_start = t_html.find('<div class="page-header">')
        if main_start == -1:
            main_start = t_html.find('<main class="main">') + len('<main class="main">')
        main_end = t_html.find('</main>')
        
        main_content = t_html[main_start:main_end]
        
        # Build new top with css
        new_top = base_top.replace('</style>', css_to_keep + '\n</style>')
        
        # In base_topbar we should maybe remove or adjust topbar for these pages?
        # Actually dashboard.html topbar has the user name and clock. 
        # But evaluar_riesgo has its own page-header. We can keep both or remove topbar.
        # Let's NOT add base_topbar if we have page-header. Or let's add it, it's nice.
        # Wait, dashboard_paciente has page-header.
        
        new_html = new_top + '\n' + main_content + '\n</main>\n' + base_html[base_html.find('<script>'):]
        
        with open(t, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"Updated {t}")

