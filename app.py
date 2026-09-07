import streamlit as st
from pathlib import Path
from PIL import Image
import pymupdf, io
from groq import Groq

st.set_page_config(page_title="Gerardo Mena Castillo - Portafolio", page_icon="🎓", layout="wide")

# API Key de Groq desde Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Raleway:ital,wght@0,400;0,600;0,800;1,400&display=swap');

:root {
    --brand: #a700ff;
    --brand-soft: #d452ff;
    --panel: #0d071b;
}

.stApp {
    background: transparent;
    color: inherit;
    font-family: "Raleway", sans-serif;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 9rem;
}

h1, h2, h3 {
    color: inherit !important;
    font-family: "Montserrat", sans-serif !important;
}

.profile-card {
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(167, 0, 255, 0.95) 0 11%, transparent 11%),
        linear-gradient(145deg, #15052e 0%, #090511 66%);
    border: 1px solid rgba(212, 82, 255, 0.55);
    border-radius: 0;
    box-shadow: 0 18px 48px rgba(30, 0, 56, 0.36);
    padding: 2.1rem 1.6rem 1.5rem;
    height: 100%;
    color: #fff;
}

.profile-card::before {
    content: "GERARDO MENA";
    position: absolute;
    top: 4.1rem;
    left: -5.6rem;
    color: rgba(255, 255, 255, 0.14);
    font: 800 1.8rem/1 "Montserrat", sans-serif;
    letter-spacing: 0.08em;
    transform: rotate(-90deg);
    white-space: nowrap;
}

.profile-card [data-testid="stImage"] {
    position: relative;
    z-index: 1;
    margin: 0.9rem 0 1.4rem 2.2rem;
}

.profile-card [data-testid="stImage"] img {
    border: 4px solid var(--brand);
    filter: grayscale(100%) contrast(1.08);
}

.eyebrow {
    color: var(--brand);
    font-size: 0.78rem;
    font-family: "Montserrat", sans-serif;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.hero-name {
    color: inherit;
    font-family: "Montserrat", sans-serif;
    font-size: clamp(2.5rem, 6vw, 5.3rem);
    font-weight: 800;
    letter-spacing: -0.06em;
    line-height: 0.9;
    margin: 0.3rem 0 1.3rem;
    text-transform: uppercase;
    text-shadow: 4px 4px 0 rgba(167, 0, 255, 0.30);
}

.hero-description {
    color: inherit;
    opacity: 0.78;
    font-size: 1.05rem;
    line-height: 1.7;
    max-width: 800px;
}

.contact-item {
    color: inherit;
    opacity: 0.78;
    font-size: 0.9rem;
    margin: 0.45rem 0;
}

.contact-item strong { color: var(--brand-soft); }

.timeline {
    position: relative;
    display: grid;
    gap: 0.8rem;
    margin-top: 1.6rem;
    padding-left: 1.5rem;
}

.timeline::before {
    content: "";
    position: absolute;
    top: 0.2rem;
    bottom: 0.2rem;
    left: 0.25rem;
    width: 2px;
    background: var(--brand);
}

.timeline-item { position: relative; }
.timeline-item::before {
    content: "";
    position: absolute;
    top: 0.35rem;
    left: -1.48rem;
    width: 0.48rem;
    height: 0.48rem;
    background: var(--brand-soft);
    border: 4px solid var(--panel);
    border-radius: 50%;
}
.timeline-item strong {
    color: var(--brand);
    font-family: "Montserrat", sans-serif;
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.timeline-item span { display: block; font-size: 0.94rem; opacity: 0.78; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.5rem;
    border-bottom: 1px solid rgba(127, 127, 127, 0.28);
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 0;
    color: inherit;
    opacity: 0.72;
    font-family: "Montserrat", sans-serif;
    font-weight: 700;
    padding: 0.7rem 1rem;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(167, 0, 255, 0.12);
    color: var(--brand);
    opacity: 1;
}

[data-testid="stChatMessage"] {
    background: rgba(127, 127, 127, 0.10);
    border-left: 3px solid var(--brand);
    border-radius: 0 12px 12px 0;
    padding: 0.35rem 0.7rem;
    margin-bottom: 0.65rem;
}

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 18px;
    width: min(90%, 820px)!important;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    background: transparent;
    padding-top: 0;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: 1px solid rgba(127, 127, 127, 0.40) !important;
    border-radius: 0 !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

@media (max-width: 700px) {
    .block-container { padding-top: 1rem; }
    .hero-name { font-size: 2.25rem; }
    .profile-card [data-testid="stImage"] { margin-left: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

carpeta = Path(__file__).resolve().parent
foto_path = carpeta / "foto.jpg"
pdf_file = carpeta / "portafolio.pdf"
if not pdf_file.exists():
    pdf_file = carpeta / "portafolio.pdf.pdf"

def dhash(image, hash_size=8):
    img = image.convert("L").resize((hash_size+1, hash_size), Image.LANCZOS)
    pixels = list(img.getdata())
    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row*(hash_size+1)+col]
            right = pixels[row*(hash_size+1)+col+1]
            diff.append('1' if left > right else '0')
    return ''.join(diff)
def hamming(s1,s2):
    return sum(c1!=c2 for c1,c2 in zip(s1,s2))

texto_extra=""; imagenes=[]; hashes_vistos=[]; hash_perfil=None
if foto_path.exists():
    try: hash_perfil=dhash(Image.open(foto_path))
    except: pass
if pdf_file.exists():
    doc=pymupdf.open(pdf_file)
    for page in doc:
        texto_extra+=page.get_text()+"\n"
        for img in page.get_images():
            try:
                base=doc.extract_image(img[0])
                if base["width"]<400 or base["height"]<300: continue
                pil=Image.open(io.BytesIO(base["image"]))
                hsh=dhash(pil)
                if any(hamming(hsh, hv)<8 for hv in hashes_vistos): continue
                if hash_perfil and hamming(hsh, hash_perfil)<12: continue
                hashes_vistos.append(hsh)
                imagenes.append(pil)
            except: pass

cv_base=(carpeta/"cv.txt").read_text(encoding="utf-8", errors="ignore") if (carpeta/"cv.txt").exists() else ""
cv_completo=cv_base+"\n\nPORTAFOLIO:\n"+texto_extra

c1,c2=st.columns([1,3])
with c1:
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    if foto_path.exists():
        st.image(Image.open(foto_path), width=180)
    st.markdown("<p class='eyebrow'>Perfil profesional · 2026</p>", unsafe_allow_html=True)
    st.markdown("**Lic. en Mercadotecnia y Comercio Digital**")
    st.markdown("<p class='contact-item'>✉️ <strong>gemeca1202@gmail.com</strong></p><p class='contact-item'>📍 Oaxaca, México</p><p class='contact-item'>🎓 Céd. Prof. 13804627</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown("<p class='eyebrow'>Portafolio interactivo · Experiencia · IA</p>", unsafe_allow_html=True)
    st.markdown("<div class='hero-name'>Gerardo<br>Mena Castillo</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-description'>Profesional con experiencia en gestión administrativa, trámites institucionales y herramientas digitales, aplicada tanto en el sector privado como en proyectos vinculados a instituciones públicas (IMSS, CFE y gobierno municipal). Combino experiencia operativa, atención a clientes institucionales y una sólida base en mercadotecnia y comercio digital.</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='timeline'>
      <div class='timeline-item'><strong>Gestión institucional</strong><span>Procesos, documentación y atención a clientes.</span></div>
      <div class='timeline-item'><strong>Marketing digital</strong><span>Contenido, plataformas y presencia digital.</span></div>
      <div class='timeline-item'><strong>Operación propia</strong><span>Más de 10 años resolviendo y liderando con autonomía.</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["💬 Conversa con mi experiencia", "📸 Portafolio visual"])
with tab1:
    st.caption("Haz una pregunta sobre mi trayectoria, habilidades, estudios o proyectos.")
    chat_container = st.container(height=500)
    with chat_container:
        if "m" not in st.session_state:
            st.session_state.m=[{"role":"assistant","content":"Hola, soy la IA de Gerardo Mena Castillo. Pregúntame sobre mi experiencia profesional."}]
        for x in st.session_state.m:
            with st.chat_message(x["role"]): st.markdown(x["content"])

    q = st.chat_input("Pregunta sobre mi experiencia...")
    if q:
        st.session_state.m.append({"role":"user","content":q})
        with chat_container:
            with st.chat_message("user"): st.markdown(q)
            with st.chat_message("assistant"):
                prompt=f"Usa SOLO esta info: {cv_completo[:12000]}\nPregunta: {q}\nResponde en primera persona como Gerardo, corto y profesional:"
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": prompt}]
                )
                ans = completion.choices[0].message.content
                st.markdown(ans)
        st.session_state.m.append({"role":"assistant","content":ans})
        st.rerun()
with tab2:
    if imagenes:
        cols=st.columns(3)
        for i,im in enumerate(imagenes):
            cols[i%3].image(im, use_container_width=True)
