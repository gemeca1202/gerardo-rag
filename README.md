# Gerardo-RAG

Un MVP educativo de RAG (Retrieval-Augmented Generation) para consultar los CV y portafolios de Gerardo Mena. No inventa datos: sus respuestas se generan a partir de los fragmentos recuperados de los PDF indexados.

## Cómo funciona

```text
CV PDF → extracción de texto → chunks con metadatos → embeddings → índice vectorial local
                                                                    ↓
pregunta → embedding de la pregunta → similitud coseno → contexto → respuesta con IA
```

- **Extracción:** `pypdf` lee el texto de cada página del PDF.
- **Chunks y metadatos:** cada fragmento guarda fuente, página, número de chunk y tipo de documento. Así cada respuesta puede rastrearse al CV.
- **Embeddings:** convierten cada fragmento y la pregunta en vectores numéricos comparables. Se usa `text-embedding-3-small` por defecto.
- **Almacenamiento y búsqueda:** los vectores viven localmente en `data/processed/index.jsonl`; la búsqueda calcula similitud coseno y recupera los mejores resultados.
- **Generación:** el modelo recibe solamente los resultados recuperados y debe declarar cuando el CV no contiene una respuesta.

## Preparación (Windows / PowerShell)

1. Copia los PDFs que quieras consultar a `data/raw/`. Cada fragmento conserva el nombre del PDF y la página de origen.
2. Crea y activa un entorno virtual:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instala las dependencias y configura la clave:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   Copy-Item .env.example .env
   ```

   Abre `.env` y reemplaza `pon_tu_clave_aqui` por tu `OPENAI_API_KEY`.

## Construir la base de conocimiento

```powershell
.\.venv\Scripts\python.exe -m gerardo_rag.cli index
```

Este paso se ejecuta cada vez que agregues o cambies un PDF. Indexa todos los PDFs de `data/raw/` y produce `data/processed/index.jsonl` y `manifest.json`.

Para indexar solamente documentos concretos:

```powershell
.\.venv\Scripts\python.exe -m gerardo_rag.cli index --files "data/raw/CV_Gerardo_Mena_INM.pdf" "data/raw/CV_Gerardo_Mena_DT.pdf"
```

## Hacer una consulta

```powershell
.\.venv\Scripts\python.exe -m gerardo_rag.cli ask "¿Qué experiencia tiene Gerardo administrando restaurantes?" --show-context
```

`--show-context` permite ver exactamente qué fragmentos recuperó el sistema antes de responder. Prueba también:

```powershell
.\.venv\Scripts\python.exe -m gerardo_rag.cli ask "¿Qué hizo en Mr. BBQ?" --show-context
.\.venv\Scripts\python.exe -m gerardo_rag.cli ask "¿Cuál es su formación académica?" --show-context
.\.venv\Scripts\python.exe -m gerardo_rag.cli ask "¿Qué proyectos ha desarrollado?" --show-context
```

## Verificación rápida

Sin necesitar una clave ni el CV, puedes comprobar la lógica de fragmentación:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Límites deliberados del MVP

El PDF debe contener texto seleccionable. Si es escaneado como imagen, primero requerirá OCR. El índice JSONL es transparente y suficiente para un CV; al incorporar cientos de documentos convendrá migrar a una base vectorial dedicada.

La integración usa el SDK oficial de OpenAI: [embeddings](https://developers.openai.com/api/reference/ruby/resources/embeddings/methods/create) y [Responses API](https://developers.openai.com/api/reference/cli/resources/responses/methods/create).
