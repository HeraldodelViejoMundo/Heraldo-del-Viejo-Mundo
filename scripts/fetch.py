"""
Genera posts de Google News para Warhammer The Old World
Resumen IA → markdown en _posts/
Requisitos: pip install feedparser markdownify openai requests
"""

from __future__ import annotations
import os, re, textwrap, datetime, hashlib, pathlib, sys

import feedparser
from markdownify import markdownify as html2md
import openai                                   # ← usa tu API key

# ---------- CONFIG ----------------------------------------------------------
FEED_URL  = "https://news.google.com/rss/search?q=%22The+Old+World%22+Warhammer&hl=en&gl=US&ceid=US:en"
POSTS_DIR = pathlib.Path("_posts")
MODEL     = "gpt-3.5-turbo-1106"
PARAS     = 3        # nº de párrafos que queremos en el resumen
openai.api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Falta OPENAI_API_KEY")
# ---------------------------------------------------------------------------

def slugify(txt):               # «mi-titulo» para el nombre de archivo
    txt = re.sub(r"[^\w\s-]", "", txt.lower())
    return re.sub(r"[\s_-]+", "-", txt).strip("-")[:50]

def md_name(dt, title):
    return f"{dt:%Y-%m-%d}-{slugify(title)}.md"

def summarize(html: str) -> str:
    prompt = textwrap.dedent(f"""
        Eres redactor de un blog de Warhammer.
        Reescribe de nuevo la noticia en español y resúmela. No debes Traducir los nombres `The Old World`, `Arcane Journal`, ni `Legacy`. 
        El texto debe empezar con un párrafo con la información más importante condensada en dos o tres líneas, de forma que sirva de resumen de la noticia.
        El resto de párrafos desarrolla la noticia con tus propias palabras. Usa como contexto la información proporcionada previamente en este blog y, si tiene sentido y fuera relevanrte, relaciona esta noticia con noticias antiguas.
        Máximo 90 palabras por párrafo. Y máximo {PARAS} párrafos.

        CONTENIDO HTML:
        {html[:4000]}
    """)
    r = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return r.choices[0].message.content.strip()

# ---------- MAIN ------------------------------------------------------------
POSTS_DIR.mkdir(exist_ok=True)
feed = feedparser.parse(FEED_URL)

for e in feed.entries:
    dt = datetime.datetime(*e.published_parsed[:6])
    fname = POSTS_DIR / md_name(dt, e.title)

    if fname.exists():          # ya publicado
        continue

    print("➕ Nuevo post:", fname.name)
    body   = summarize(e.summary)
    backup = html2md(e.summary)

    md = textwrap.dedent(f"""\
        ---
        layout: post
        title: "{e.title.replace('"', '\\"')}"
        date: {dt.isoformat()}
        categories: noticias
        original_url: {e.link}
        ---

        {body}

        [Leer más en la fuente ➜]({e.link})

        ---
        *Copia de seguridad en markdown (auto-generada)*

        {backup}
    """)

    fname.write_text(md, encoding="utf-8")
print("🔥 Terminado")
