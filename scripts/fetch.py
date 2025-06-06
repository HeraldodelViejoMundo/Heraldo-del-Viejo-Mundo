"""
Bot de titulares — Warhammer The Old World
Lee Google News, resume con GPT-3.5 y crea Markdown en _posts/.

Requisitos en el workflow:
    pip install feedparser markdownify openai requests
"""
from __future__ import annotations
import os, re, datetime, textwrap, pathlib, sys
from urllib.parse import urlparse

import feedparser
from markdownify import markdownify as html2md
import openai

# ---------- CONFIG ----------------------------------------------------------
FEED_URL = ("https://news.google.com/rss/search?"
            "q=%22The+Old+World%22+Warhammer&hl=en&gl=US&ceid=US:en")

POSTS_DIR   = pathlib.Path("_posts")
MODEL       = "gpt-3.5-turbo-1106"
DAYS_LIMIT  = 7               # sólo noticias ≤ 7 días
PARAS       = 3               # nº de párrafos del resumen

openai.api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Falta OPENAI_API_KEY")
# ---------------------------------------------------------------------------


def slugify(txt: str) -> str:
    txt = re.sub(r"[^\w\s-]", "", txt.lower())
    return re.sub(r"[\s_-]+", "-", txt).strip("-")[:50]


def md_name(dt: datetime.datetime, title: str) -> str:
    return f"{dt:%Y-%m-%d}-{slugify(title)}.md"


def summarize(html: str) -> str:
    prompt = textwrap.dedent("""
        Eres redactor de un blog de Warhammer.
        Reescribe la noticia en español, resumiéndola un poco. No traduzcas los
        nombres `The Old World`, `Arcane Journal` ni `Legacy`.
        Empieza con un párrafo (2-3 líneas) de resumen. Después desarrolla la
        noticia en {paras} párrafos (máx. 120 palabras cada uno), enlazando con
        noticias antiguas si procede.
        ---
        CONTENIDO HTML (recortado):
        {html}
        ---
    """).format(html=html[:4000], paras=PARAS)

    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()



# ---------- MAIN ------------------------------------------------------------
POSTS_DIR.mkdir(exist_ok=True)
feed = feedparser.parse(FEED_URL)

for e in feed.entries:
    pub_dt = datetime.datetime(*e.published_parsed[:6])

    # descarta lo que sea demasiado viejo
    if (datetime.datetime.utcnow() - pub_dt).days > DAYS_LIMIT:
        continue

    fname = POSTS_DIR / md_name(pub_dt, e.title)
    if fname.exists():
        continue  # ya publicado
        continue

    print("➕ Nuevo post:", fname.name)

    body_md   = summarize(e.summary)
    backup_md = html2md(e.summary)

    md = textwrap.dedent(f"""\
        ---
        layout: post
        title: "{e.title.replace('"', '\\"')}"
        date: {pub_dt.isoformat()}
        last_modified_at: {datetime.datetime.utcnow().isoformat()}
        categories: noticias
        original_url: {e.link}
        ---

        {body_md}

        [Leer más en la fuente ➜]({e.link})

        ---
        *Copia de seguridad en markdown (auto-generada)*

        {backup_md}
    """)

    fname.write_text(md, encoding="utf-8")
print("🔥 Terminado")
