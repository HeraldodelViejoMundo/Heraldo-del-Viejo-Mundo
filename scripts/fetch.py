"""
Genera posts de Google News para Warhammer The Old World
Resumen IA → markdown en _posts/
Requisitos: pip install feedparser markdownify openai requests
"""
from __future__ import annotations
import os, re, textwrap, datetime, pathlib, sys

import feedparser
from markdownify import markdownify as html2md
import openai                        # ← usa tu API-key

# ---------- CONFIG ----------------------------------------------------------
FEED_URL  = (
    "https://news.google.com/rss/search?q=%22The+Old+World%22+Warhammer"
    "&hl=en&gl=US&ceid=US:en"
)
POSTS_DIR = pathlib.Path("_posts")
MODEL     = "gpt-3.5-turbo-1106"

openai.api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Falta OPENAI_API_KEY")
# ---------------------------------------------------------------------------


def slugify(txt: str) -> str:
    txt = re.sub(r"[^\w\s-]", "", txt.lower())
    return re.sub(r"[\s_-]+", "-", txt).strip("-")[:50]


def md_name(dt: datetime.datetime, title: str) -> str:
    return f"{dt:%Y-%m-%d}-{slugify(title)}.md"


# ---------- IA --------------------------------------------------------------
def summarize(html: str) -> str:
    prompt = textwrap.dedent("""
        Eres redactor de un blog de Warhammer.
        Reescribe la noticia en español y resúmela un poco. No traduzcas los nombres
        `The Old World`, `Arcane Journal` ni `Legacy`.
        Empieza con un párrafo resumen (2–3 líneas). Desarrolla luego la noticia
        con tus palabras (máx. 120 palabras por párrafo), enlazando con posts
        anteriores si procede.
        ---
        CONTENIDO HTML (recortado):
        {html}
        ---
    """).format(html=html[:4000])

    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()


# ---------- MAIN ------------------------------------------------------------
POSTS_DIR.mkdir(exist_ok=True)
feed = feedparser.parse(FEED_URL)

for entry in feed.entries:
    dt     = datetime.datetime(*entry.published_parsed[:6])
    fname  = POSTS_DIR / md_name(dt, entry.title)
    if fname.exists():
        continue  # ya publicado

    print("➕ Nuevo post:", fname.name)

    body    = summarize(entry.summary)
    backup  = html2md(entry.summary)
    # ⚠️ SIN barras invertidas: sustituimos " por '
    safe_title = entry.title.replace('"', "'")

    md = textwrap.dedent(f"""\
        ---
        layout: post
        title: "{safe_title}"
        date: {dt.isoformat()}
        categories: noticias
        original_url: {entry.link}
        ---

        {body}

        [Leer más en la fuente ➜]({entry.link})

        ---
        *Copia de seguridad en markdown (auto-generada)*

        {backup}
    """)

    fname.write_text(md, encoding="utf-8")

print("🔥 Terminado")
