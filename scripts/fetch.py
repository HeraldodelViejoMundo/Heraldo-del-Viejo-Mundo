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
DAYS_LIMIT  = 7               # sólo noticias de la última semana
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
feed     = feedparser.parse(FEED_URL)
now_utc  = datetime.datetime.utcnow()
lim_date = now_utc - datetime.timedelta(days=DAYS_LIMIT)

for entry in feed.entries:
    pub_dt = datetime.datetime(*entry.published_parsed[:6])

    # sólo última semana
    if pub_dt < lim_date:
        continue

    fname = POSTS_DIR / md_name(pub_dt, entry.)
    if fname.exists():
        continue  # ya publicado

    print("➕ Nuevo post:", fname.name)

    body    = summarize(entry.summary)
    backup  = html2md(entry.summary)
    safe_ = entry..replace('"', "'")
    source   = urlparse(entry.link).netloc.replace("www.", "")

    md = textwrap.dedent(f"""\
---          # ← primera línea
layout: post
title: "{e.title.replace('"', '\\"')}"
date: {dt.isoformat()}
last_modified_at: {datetime.datetime.utcnow().isoformat()}
categories: noticias
original_url: {e.link}
---

{body}

[Leer la noticia completa ↗]({e.link})

<!-- Copia de seguridad (HTML → Markdown) -->
{backup}
""")

    fname.write_text(md, encoding="utf-8")

print("🔥 Terminado")
