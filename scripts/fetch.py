"""
Lee el RSS oficial de Warhammer Community (sección The Old World),
resume cada noticia con la API de OpenAI y genera un archivo Markdown
en la carpeta _posts/ si aún no existe.

Requisitos instalados en el workflow:
  pip install feedparser markdownify openai requests
"""

from __future__ import annotations
import os, re, hashlib, datetime, textwrap, pathlib, sys

import feedparser                    # RSS
from markdownify import markdownify as html2md
import openai                        # Resumen IA

# --- Configuración ---------------------------------------------------------

FEED_URL = "https://www.warhammer-community.com/category/old-world/feed/"
POSTS_DIR = pathlib.Path("_posts")
CATEGORY  = "noticias"
MODEL     = "gpt-3.5-turbo-1106"
BULLETS   = 4                         # nº de viñetas en el resumen

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    print("OPENAI_API_KEY no definido; saliendo.")
    sys.exit(0)

# --- Utilidades ------------------------------------------------------------

def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:50]

def md_filename(dt: datetime.datetime, title: str) -> str:
    slug = slugify(title)
    return f"{dt:%Y-%m-%d}-{slug}.md"

def summarize(html: str) -> str:
    """Devuelve un resumen en viñetas en español."""
    prompt = textwrap.dedent(f"""
        Eres un redactor especializado en Warhammer. Resume la siguiente
        noticia en {BULLETS} viñetas concisas en español (máx. 30 palabras cada una).

        CONTENIDO HTML ORIGINAL:
        ---
        {html[:4000]}
        ---
    """)
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role":"user","content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()

# --- Flujo principal -------------------------------------------------------

POSTS_DIR.mkdir(exist_ok=True)

feed = feedparser.parse(FEED_URL)
added = 0

for entry in feed.entries:
    # Fecha UTC del entry
    published = datetime.datetime(*entry.published_parsed[:6])
    fname = POSTS_DIR / md_filename(published, entry.title)

    if fname.exists():
        continue  # ya publicado

    print("➕ Nuevo post:", fname.name)

    # Resumen IA
    bullet_md = summarize(entry.summary)

    # Conversión HTML→Markdown del cuerpo (fallback si IA falla)
    body_md = html2md(entry.summary)

    # --- Front-matter Jekyll ---
    header = textwrap.dedent(f"""\
        ---
        layout: post
        title: "{entry.title.replace('"','\\"')}"
        date: {published.isoformat()}
        categories: {CATEGORY}
        original_url: {entry.link}
        ---
    """)

    content = "\n\n".join([header, bullet_md, "\n---\n", body_md])

    fname.write_text(content, encoding="utf-8")
    added += 1

print(f"Posts añadidos: {added}")
