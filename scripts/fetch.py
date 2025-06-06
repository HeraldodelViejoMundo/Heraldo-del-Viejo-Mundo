"""
Bot de titulares — Warhammer The Old World
Lee Google News, resume con GPT-3.5 y crea archivos Markdown en _posts/.

Requisitos en el workflow:
    pip install feedparser markdownify openai requests
"""

from __future__ import annotations
import os, re, datetime as dt, textwrap, pathlib, sys

import feedparser
from markdownify import markdownify as html2md
import openai

# ── CONFIG ────────────────────────────────────────────────────────────────
FEED_URL = (
    "https://news.google.com/rss/search?"
    "q=%22The+Old+World%22+Warhammer&hl=en&gl=US&ceid=US:en"
)

POSTS_DIR  = pathlib.Path("_posts")
MODEL      = "gpt-3.5-turbo-1106"
DAYS_LIMIT = 7          # solo noticias ≤ 7 días
PARAS      = 3          # párrafos en el resumen

openai.api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Falta OPENAI_API_KEY")
# ──────────────────────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[\s_-]+", "-", text).strip("-")[:50]


def md_filename(d: dt.datetime, title: str) -> str:
    return f"{d:%Y-%m-%d}-{slugify(title)}.md"


def summarize(html: str) -> str:
    prompt = textwrap.dedent("""
        Eres redactor de un blog de Warhammer.
        Reescribe la siguiente noticia en español: primero un párrafo-resumen
        (2-3 líneas). Después desarrolla la noticia en un máximo de {paras} párrafos
        (≤90 palabras cada uno). No traduzcas los términos `The Old World`,
        `Arcane Journal` ni `Legacy`. 
        Usa como contexto tus conocimientos de The Old World y lo publicado en este blog. 
        Si procede, relaciona con noticias previas.

        ---
        CONTENIDO HTML ORIGINAL (recortado):
        {html}
        ---
    """).format(html=html[:4000], paras=PARAS)

    resp = openai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()


# ── MAIN ──────────────────────────────────────────────────────────────────
POSTS_DIR.mkdir(exist_ok=True)
feed = feedparser.parse(FEED_URL)

for entry in feed.entries:
    pub_dt = dt.datetime(*entry.published_parsed[:6])

    if (dt.datetime.utcnow() - pub_dt).days > DAYS_LIMIT:
        continue  # demasiado antigua

    fname = POSTS_DIR / md_filename(pub_dt, entry.title)
    if fname.exists():
        continue  # ya publicada

    print("➕ Nuevo post:", fname.name)

    body_md   = summarize(entry.summary)
    backup_md = html2md(entry.summary)
    safe_title = entry.title.replace('"', "'")   # ← sin barra invertida

    # bloque YAML con dedent() y formato correcto
    md = textwrap.dedent("""\
        ---
        layout: post
        title: "{title}"
        date: {date}
        last_modified_at: {mod}
        categories: noticias
        original_url: {url}
        ---

        {body}

        [Leer la noticia completa ➜]({url})

        ---
        *Copia de seguridad (Markdown auto-generado)*

        {backup}
    """).format(
        title=safe_title,
        date=pub_dt.isoformat(),
        mod=dt.datetime.utcnow().isoformat(),
        url=entry.link,
        body=body_md,
        backup=backup_md,
    )

    fname.write_text(md, encoding="utf-8")

print("🔥 Terminado")
