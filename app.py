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
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    width: 60%!important;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9999;
    background: #0e1117;
    padding-top: 10px;
}
.block-container { padding-bottom: 100px; }
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
    if foto_path.exists():
        st.image(Image.open(foto_path), width=180)
    st.markdown("**Lic. en Mercadotecnia y Comercio Digital**\n\n📧 gemeca1202@gmail.com\n\nCéd. Prof. 13804627\n\nOaxaca, México")
with c2:
    st.title("GERARDO MENA CASTILLO")
    st.markdown("**Lic. en Mercadotecnia y Comercio Digital**")
    st.markdown("""
    Profesional con experiencia en gestión administrativa, trámites institucionales y herramientas digitales,
    aplicada tanto en el sector privado como en proyectos vinculados a instituciones públicas (IMSS, CFE,
    gobierno municipal). He gestionado procesos, documentación y clientes institucionales, y cuento con
    experiencia práctica en plataformas digitales (Google Ads, Google My Business, gestión de contenido y redes).
    Complemento esta base con más de 10 años liderando operaciones propias, con capacidad demostrada de aprender
    procesos técnicos nuevos y resolverlos con autonomía. Licenciado en Mercadotecnia y Comercio Digital,
    con cédula profesional vigente.
    """)

tab1, tab2 = st.tabs(["💬 Chatea con mi CV", "📸 Evidencias"])
with tab1:
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