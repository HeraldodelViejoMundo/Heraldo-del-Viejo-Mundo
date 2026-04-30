---
layout: default
title: Vídeos
permalink: /videos/
---

<a href="{{ '/' | relative_url }}">
  <img src="{{ '/assets/bannerheraldo.png' | relative_url }}" alt="Cabecera El Heraldo del Viejo Mundo" style="width:100%; height:auto; max-height:240px; object-fit:contain; display:block; margin-bottom: 2em;">
</a>

<div style="max-width: 1200px; margin: 0 auto; padding: 0 2em;">

<h1 style="text-align: center; margin-bottom: 0.2em;">Vídeos</h1>
<p style="text-align: center; color: #666; margin-top: 0; margin-bottom: 2em;">
  Lo más reciente de los canales de la comunidad española sobre <em>Warhammer: The Old World</em> y <em>Warhammer Fantasy</em>.
</p>

{%- comment -%}
  Whitelist de canales (mismo orden que en video_bot.py).
  Cualquier vídeo cuyo `channel:` no esté en esta lista se ignora.
{%- endcomment -%}
{%- assign whitelist = "La Forja del Fénix|La Alianza del Viejo Mundo|13th Warrior|Moria Wargames|La Taberna del Enano|La Taberna del Guerrero|La Posada del Martillo|Juegos y Dados|Leyendas en Miniatura|La Escotilla Estaliana Podcast" | split: "|" -%}

{%- assign sorted_videos = site.videos | sort: "date" | reverse -%}

{%- for canal in whitelist -%}
  {%- assign canal_lower = canal | downcase -%}
  {%- assign canal_videos = "" | split: "" -%}
  {%- for v in sorted_videos -%}
    {%- assign v_canal = v.channel | downcase -%}
    {%- if v_canal == canal_lower -%}
      {%- assign canal_videos = canal_videos | push: v -%}
    {%- endif -%}
  {%- endfor -%}
  {%- if canal_videos.size > 0 -%}

<section style="margin-bottom: 3em;">
  <h2 style="border-bottom: 2px solid #b87333; padding-bottom: 0.3em; margin-bottom: 1em;">
    {{ canal }} <span style="color: #999; font-size: 0.7em; font-weight: normal;">({{ canal_videos.size }} vídeo{% if canal_videos.size != 1 %}s{% endif %})</span>
  </h2>

  <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.2em;">
    {%- for v in canal_videos limit: 8 -%}
    <a href="{{ v.url | relative_url }}" style="display: block; text-decoration: none; color: inherit; border: 1px solid #e0e0e0; border-radius: 6px; overflow: hidden; transition: box-shadow 0.2s;" onmouseover="this.style.boxShadow='0 4px 12px rgba(0,0,0,0.15)'" onmouseout="this.style.boxShadow='none'">
      {%- if v.thumbnail -%}
      <img src="{{ v.thumbnail }}" alt="{{ v.title | escape }}" loading="lazy" style="width: 100%; height: 160px; object-fit: cover; display: block;">
      {%- endif -%}
      <div style="padding: 0.7em 0.9em;">
        <div style="font-size: 0.8em; color: #888; margin-bottom: 0.3em;">{{ v.date | date: "%d/%m/%Y" }}</div>
        <div style="font-weight: 600; font-size: 0.95em; line-height: 1.3;">
          {{ v.title | remove: "Nuevo vídeo de " | remove: canal | remove: ": " | strip | truncate: 90 }}
        </div>
      </div>
    </a>
    {%- endfor -%}
  </div>

  {%- if canal_videos.size > 8 -%}
  <p style="margin-top: 0.8em; font-size: 0.9em; color: #666;">
    Mostrando los 8 más recientes de {{ canal_videos.size }}.
  </p>
  {%- endif -%}
</section>

  {%- endif -%}
{%- endfor -%}

</div>
