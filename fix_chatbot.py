import os

chatbot_file = 'E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/chatbot.html'
eval_file = 'E:/Proyectos Next/Zumedical/sistema_prenatal/templates/paciente/evaluar_riesgo.html'

chat_script = """
// ── CHATBOT SCRIPT ─────────────────────────────────────────────────────────
const ENDPOINT   = '{{ chatbot_endpoint }}';
const CSRF_TOKEN = '{{ csrf_token }}';
const USER_INICIALES = '{% if request.user.first_name %}{{ request.user.first_name|slice:":1" }}{{ request.user.last_name|slice:":1" }}{% else %}{{ request.user.username|slice:":1"|upper }}{% endif %}'.toUpperCase() || 'Yo';

const messagesEl = document.getElementById('chat-messages');

function scrollBottom() {
  setTimeout(() => { messagesEl.scrollTop = messagesEl.scrollHeight; }, 80);
}

function addMsg(tipo, html) {
  const wrap = document.createElement('div');
  wrap.className = `msg ${tipo}`;

  const av = document.createElement('div');
  av.className = 'msg-av';
  av.textContent = tipo === 'bot' ? '🤱' : USER_INICIALES;

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = html;

  wrap.appendChild(av);
  wrap.appendChild(bubble);
  messagesEl.appendChild(wrap);
  scrollBottom();
  return wrap;
}

function addOpciones(botones, tipo = 'btn') {
  const wrap = document.createElement('div');
  wrap.className = 'opciones';
  botones.forEach(b => {
    const btn = document.createElement('button');
    btn.className = tipo === 'cat' ? 'btn-opcion cat' : 'btn-opcion';
    btn.innerHTML = b.label;
    btn.onclick = () => { disableOpciones(); enviar(b.estado, b.label); };
    wrap.appendChild(btn);
  });
  messagesEl.appendChild(wrap);
  scrollBottom();
}

function addVolver() {
  const wrap = document.createElement('div');
  wrap.className = 'opciones';
  const btn = document.createElement('button');
  btn.className = 'btn-volver';
  btn.textContent = '← Volver al menú de ayuda';
  btn.onclick = () => { disableOpciones(); enviar('volver', 'Volver al menú'); };
  wrap.appendChild(btn);
  messagesEl.appendChild(wrap);
  scrollBottom();
}

function disableOpciones() {
  messagesEl.querySelectorAll('.btn-opcion,.btn-volver').forEach(b => {
    b.disabled = true;
    b.style.opacity = '.45';
    b.style.cursor = 'default';
  });
}

function showTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'msg bot';
  wrap.id = 'typing-indicator';
  wrap.innerHTML = `
    <div class="msg-av">🤱</div>
    <div class="typing"><span></span><span></span><span></span></div>
  `;
  messagesEl.appendChild(wrap);
  scrollBottom();
}

function hideTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

async function enviar(estado, textoUsuario = '') {
  if (textoUsuario && textoUsuario !== 'inicio' && textoUsuario !== 'volver') {
    addMsg('user', textoUsuario);
  }

  showTyping();

  try {
    const res = await fetch(ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN,
      },
      body: JSON.stringify({ estado }),
    });
    const data = await res.json();
    hideTyping();
    manejarRespuesta(data);
  } catch (e) {
    hideTyping();
    addMsg('bot', '⚠️ Error de conexión. Por favor intenta nuevamente.');
  }
}

function manejarRespuesta(data) {
  if (data.tipo === 'bienvenida' || data.tipo === 'categorias') {
    addMsg('bot', data.mensaje);
    if (data.categorias && data.categorias.length) {
      addOpciones(
        data.categorias.map(c => ({
          label: `${c.emoji} ${c.nombre}`,
          estado: `cat:${c.slug}`,
        })),
        'cat'
      );
    }
  } else if (data.tipo === 'preguntas') {
    addMsg('bot', data.mensaje);
    if (data.preguntas && data.preguntas.length) {
      addOpciones(
        data.preguntas.map(p => ({ label: p.pregunta, estado: `faq:${p.id}` }))
      );
    }
    addVolver();
  } else if (data.tipo === 'respuesta') {
    addMsg('bot', data.mensaje);
    addVolver();
  } else {
    addMsg('bot', data.mensaje || '⚠️ Opción no reconocida.');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  enviar('inicio');
});
"""

# Fix chatbot.html
with open(chatbot_file, 'r', encoding='utf-8') as f:
    chat_html = f.read()

# Replace page-header
old_header_chat = """<div class="page-header">
    <p class="sub">Inteligencia Artificial  Prenatal</p>
    <h1>Asistente Virtual</h1>
  </div>"""

new_header_chat = """<div class="page-header" style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
    <div>
        <p class="sub">Inteligencia Artificial • Prenatal</p>
        <h1>Asistente Virtual</h1>
    </div>
    <a href="{% url 'paciente_dashboard' %}" class="btn-agendar" style="background:var(--white); color:var(--mg); border:1px solid var(--mg-border);"><i class="fa-solid fa-arrow-left"></i> Volver a Mi embarazo</a>
  </div>"""

chat_html = chat_html.replace(old_header_chat, new_header_chat)

# Sometimes encoding makes " Prenatal" instead of "• Prenatal". Let's use regex to replace safely.
import re
chat_html = re.sub(r'<div class="page-header">.*?<h1>Asistente Virtual</h1>\s*</div>', new_header_chat, chat_html, flags=re.DOTALL)

# Insert the script before </script>
# Actually, I'll insert it after <script>
script_pos = chat_html.find('<script>')
if script_pos != -1:
    chat_html = chat_html[:script_pos + 8] + '\n' + chat_script + '\n' + chat_html[script_pos + 8:]

with open(chatbot_file, 'w', encoding='utf-8') as f:
    f.write(chat_html)


# Fix evaluar_riesgo.html
with open(eval_file, 'r', encoding='utf-8') as f:
    eval_html = f.read()

new_header_eval = """<div class="page-header" style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem;">
    <div>
        <p class="sub">Inteligencia Artificial • Análisis clínico prenatal</p>
        <h1>Evaluación de Riesgo Gestacional</h1>
    </div>
    <a href="{% url 'paciente_dashboard' %}" class="btn-agendar" style="background:var(--white); color:var(--mg); border:1px solid var(--mg-border);"><i class="fa-solid fa-arrow-left"></i> Volver a Mi embarazo</a>
  </div>"""

eval_html = re.sub(r'<div class="page-header">.*?<h1>Evaluaci.n de Riesgo Gestacional</h1>\s*</div>', new_header_eval, eval_html, flags=re.DOTALL)

with open(eval_file, 'w', encoding='utf-8') as f:
    f.write(eval_html)

print("Done restoring chatbot script and adding Volver buttons")
