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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root {
    --brand: #0b5cab;
}

.stApp {
    background: transparent;
    color: inherit;
    font-family: "DM Sans", sans-serif;
}

.block-container {
    max-width: 1180px;
    padding-top: 3rem;
    padding-bottom: 9rem;
}

h1, h2, h3 {
    color: inherit !important;
    font-family: "Playfair Display", serif !important;
}

.profile-card {
    background: rgba(127, 127, 127, 0.10);
    border: 1px solid rgba(127, 127, 127, 0.28);
    border-radius: 22px;
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.12);
    padding: 1.4rem;
    height: 100%;
}

.eyebrow {
    color: var(--brand);
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.hero-name {
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 700;
    line-height: 1.02;
    margin: 0.2rem 0 0.75rem;
}

.hero-description {
    color: inherit;
    opacity: 0.78;
    font-size: 1.05rem;
    line-height: 1.75;
    max-width: 760px;
}

.contact-item {
    color: inherit;
    opacity: 0.78;
    font-size: 0.9rem;
    margin: 0.45rem 0;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0.5rem;
    border-bottom: 1px solid rgba(127, 127, 127, 0.28);
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    color: inherit;
    opacity: 0.72;
    font-weight: 600;
    padding: 0.7rem 1rem;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(127, 127, 127, 0.16);
    color: var(--brand);
    opacity: 1;
}

[data-testid="stChatMessage"] {
    background: rgba(127, 127, 127, 0.10);
    border: 1px solid rgba(127, 127, 127, 0.22);
    border-radius: 16px;
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
    border-radius: 14px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
}

@media (max-width: 700px) {
    .block-container { padding-top: 1.5rem; }
    .hero-name { font-size: 2.25rem; }
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
    st.markdown("<p class='eyebrow'>Perfil profesional</p>", unsafe_allow_html=True)
    st.markdown("**Lic. en Mercadotecnia y Comercio Digital**")
    st.markdown("<p class='contact-item'>✉️ gemeca1202@gmail.com</p><p class='contact-item'>📍 Oaxaca, México</p><p class='contact-item'>🎓 Céd. Prof. 13804627</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown("<p class='eyebrow'>Portafolio · Experiencia · Conversación</p>", unsafe_allow_html=True)
    st.markdown("<div class='hero-name'>Gerardo Mena<br>Castillo</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-description'>Profesional con experiencia en gestión administrativa, trámites institucionales y herramientas digitales, aplicada tanto en el sector privado como en proyectos vinculados a instituciones públicas (IMSS, CFE y gobierno municipal). Combino experiencia operativa, atención a clientes institucionales y una sólida base en mercadotecnia y comercio digital.</div>", unsafe_allow_html=True)

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
