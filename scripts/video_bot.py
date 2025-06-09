import os
import datetime as dt
from dotenv import load_dotenv
load_dotenv(dotenv_path="/opt/oldworldbot/.env")
from googleapiclient.discovery import build
from dateutil import parser
from pathlib import Path
import openai
import sys
import hashlib

def file_has_changed(path, new_content):
    if not path.exists():
        return True
    current_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    new_hash = hashlib.sha256(new_content.encode("utf-8")).hexdigest()
    return current_hash != new_hash

# API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY") or sys.exit("Falta OPENAI_API_KEY")

# Canales permitidos y sus IDs
CHANNELS = {
    "La Alianza del Viejo Mundo": "UClg_z1cKlfVTHVOPK2kzZhQ",
    "13th Warrior": "UCYOhXS04iLg68Sro80yF_1w",
    "Moria Wargames": "UCcQsRY8wmVbBjtrnhWuL9pQ",
    "La Taberna del Enano": "UCVB8MdV9iUJBdcqA7TRVI2g",
    "La Taberna del Guerrero": "UCzyrJXBT5KP6kFPMHQnJ8nQ",
    "La Posada del Martillo": "UCuRsk2Iq9PZoC3XPLAPePEQ",
    "Juegos y Dados": "UCKYcuuzvrqrPobA1poIhOBw",
    "Leyendas en Miniatura": "UCbs4BdIbYNqb5zWPt8qYdGQ",
    "La Escotilla Estaliana Podcast": "UCnuFKtPyiIav80gPpPFdMiQ",
}

BLACKLIST = {"UCa6Kz3T7V339OWFvovQKm9Q"}  # GS Wargames

YOUTUBE = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
POSTS_DIR = Path("/opt/oldworldbot/posts")
POSTS_DIR.mkdir(parents=True, exist_ok=True)

def gpt_generate_intro(title, channel):
    prompt = f"""
Este es el título de un vídeo publicado en el canal «{channel}»:

«{title}»

Redacta una breve introducción (2–4 líneas) para un blog de Warhammer llamado «El Heraldo del Viejo Mundo».
No inventes nada. No traduzcas nada que no esté traducido en el título y especialmente no traduzcas Arcane Journal ni The Old World cuando se refiera al juego.
Solo puedes deducir o interpretar con cautela lo que se intuye a partir del título.
El tono debe ser informativo. Evita repetir el título.
Los temas más comunes son:
Video Informes: suele explicitarlo o poner el nombre de dos ejércitos y los puntos a los que se juega
Trasfondo: suele usar esta palabra (trasfondo) o nombrar un personaje o evento de warhammer fantasy
Tutoriales: explican una o más reglas o situaciones.
Podacast: usa este nombre como parte del título
Noticias: nombran temas de actualidad, lanzamientos de miniaturas o libros, torneos o eventos futuros.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ Error al llamar a GPT para resumen de vídeo:", e)

        return ""

def fetch_latest_videos(channel_name, channel_id):
    now = dt.datetime.utcnow()
    one_hour_ago = now - dt.timedelta(hours=6)
    published_after = one_hour_ago.isoformat("T") + "Z"

    res = YOUTUBE.search().list(
        part="snippet",
        channelId=channel_id,
        publishedAfter=published_after,
        type="video",
        order="date",
        maxResults=5,
    ).execute()
    print(f"[{channel_name}] Vídeos encontrados: {len(res.get('items', []))}")

    for item in res.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published_at = parser.isoparse(item["snippet"]["publishedAt"])
        print(f"→ {title} — publicado en {published_at}")

        # Verificar si ya existe el archivo .md
        slug = f"{published_at.strftime('%Y-%m-%d')}-yt-{video_id}.md"
        path = POSTS_DIR / slug
        if path.exists():
            print(f"⏩ Vídeo ya procesado previamente: {title}")
            continue

        intro = gpt_generate_intro(title, channel_name)
        url = f"https://www.youtube.com/watch?v={video_id}"
        date_str = published_at.isoformat()
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        embed = f"https://www.youtube.com/embed/{video_id}"

        md = f"""---
layout: post
title: "{title}"
date: {date_str}
categories: videos
video_url: {url}
channel: "{channel_name}"
thumbnail: {thumbnail}
excerpt: >
  {intro}
---

## {title}

<iframe width="100%" height="400" src="{embed}" frameborder="0" allowfullscreen></iframe>

📅 Publicado el {published_at.strftime('%d/%m/%Y a las %H:%M')}
🔗 [Ver en YouTube]({url})
"""

        if not file_has_changed(path, md):
            print("📭 Sin cambios detectados. No se reescribe:", path.name)
            continue

        path.write_text(md, encoding="utf-8")
        print("✅ Vídeo procesado:", path.name)

def main():
    from datetime import datetime
    import subprocess, shutil

    with open("/opt/oldworldbot/cron.log", "a") as log:
        log.write(f"🕒 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ▶️ video_bot.py iniciado\n")

    for name, cid in CHANNELS.items():
        if cid not in BLACKLIST:
            fetch_latest_videos(name, cid)

    with open("/opt/oldworldbot/cron.log", "a") as log:
        log.write(f"✅ [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] video_bot.py finalizado\n")

    # ✅ Mover los .md y publicar cambios
    REPO_DIR = "/opt/Heraldo-del-Viejo-Mundo"
    TARGET_DIR = Path(REPO_DIR) / "_posts"

    def publish_file(md_path):
        target = TARGET_DIR / md_path.name
        shutil.move(md_path, target)
        subprocess.run(["git", "-C", REPO_DIR, "add", str(target)], check=True)

    for path in POSTS_DIR.glob("*.md"):
        publish_file(path)

    # Hacer commit solo si hay cambios
    r = subprocess.run(["git", "-C", REPO_DIR, "diff", "--cached", "--quiet"])
    if r.returncode != 0:  # hay cambios
        msg = f"Vídeos auto ({datetime.utcnow().isoformat(timespec='seconds')})"
        subprocess.run(["git", "-C", REPO_DIR, "commit", "-m", msg], check=True)
        subprocess.run(["git", "-C", REPO_DIR, "push", "origin", "main"], check=True)

if __name__ == "__main__":
    main()
