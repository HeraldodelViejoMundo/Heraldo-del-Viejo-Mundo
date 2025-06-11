#!/usr/bin/env python3
"""
Añade title_original y title_translated a los posts que aún no lo tengan.
   • Toma el valor existente de `title:` como título original (inglés).
   • Cambia `title:` a "Hoy en Warhammer Community".
   • Deja title_translated como "{{pendiente}}" para rellenar después.
Hace copia .bak de cada archivo modificado.
"""

from pathlib import Path
import re, shutil

POSTS = Path("_posts")

for md in POSTS.glob("*.md"):
    text = md.read_text(encoding="utf-8")

    # saltar si ya está actualizado
    if "title_original:" in text:
        continue

    # 1) extraer el título original del front-matter
    m = re.search(r'^title:\s*"([^"]+)"', text, re.M)
    if not m:
        print(f"⚠️  No se encontró campo title en {md.name}")
        continue
    original = m.group(1).strip()

    # 2) construir los nuevos campos
    new_lines = (
        'title: "Hoy en Warhammer Community"\n'
        f'title_original: "{original.replace(chr(34), chr(39))}"\n'
        'title_translated: "{{pendiente}}"'
    )

    # 3) insertar y reemplazar dentro del front-matter
    text = re.sub(r'^title:.*$', new_lines, text, 1, re.M)

    # 4) copia de seguridad y guardar
    shutil.copy(md, md.with_suffix(".bak"))
    md.write_text(text, encoding="utf-8")
    print(f"✅  Actualizado {md.name}")

print("Hecho.")
