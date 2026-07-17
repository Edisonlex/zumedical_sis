import re

with open('E:/Proyectos Next/Zumedical/sistema_prenatal/paciente_general/templates/paciente_general/dashboard.html', 'r', encoding='utf-8') as f:
    base_html = f.read()

with open('E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/dashboard_paciente.html', 'r', encoding='utf-8') as f:
    pac_html = f.read()

# Extract top part of base_html up to <!-- MAIN -->
base_top = base_html[:base_html.find('<!-- MAIN -->') + len('<!-- MAIN -->\n<main class="main">\n')]
base_topbar = base_html[base_html.find('<!-- TOPBAR -->'):base_html.find('<!-- HERO BANNER -->')]

# Extract specific CSS from pac_html that we need to keep
css_to_keep = pac_html[pac_html.find('/* ── SECTION TITLE ── */'):pac_html.find('/* ── RESPONSIVE ── */')]

# Add the CSS to base_top
base_top = base_top.replace('</style>', css_to_keep + '\n</style>')

# Fix the active class in the sidebar of base_top
base_top = base_top.replace('class="nav-item active"', 'class="nav-item"')
# Find the Mi embarazo link and make it active
base_top = base_top.replace('href="{% url \'paciente_dashboard\' %}" class="nav-item"', 'href="{% url \'paciente_dashboard\' %}" class="nav-item active"')

# Now for the main content from pac_html
pac_main_start = pac_html.find('<!-- MENSAJES DJANGO -->')
pac_main_end = pac_html.find('</main>')

pac_main_content = pac_html[pac_main_start:pac_main_end]

# New HTML
new_html = base_top + '\n' + base_topbar + '\n' + pac_main_content + '\n</main>\n' + base_html[base_html.find('<script>'):]

with open('E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/dashboard_paciente.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
print('Rewrite successful')
