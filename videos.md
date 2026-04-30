---
layout: default
title: Vídeos
permalink: /videos/
---

<style>
  /* === Estética Viejo Mundo para la sección de Vídeos === */
  .vm-page {
    background-color: #f4ecd8;
    background-image:
      radial-gradient(ellipse at top left, rgba(139, 90, 43, 0.08) 0%, transparent 60%),
      radial-gradient(ellipse at bottom right, rgba(74, 46, 14, 0.08) 0%, transparent 60%),
      url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.27 0 0 0 0 0.18 0 0 0 0 0.07 0 0 0 0.06 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
    color: #3a2410;
    font-family: 'Cormorant Garamond', 'EB Garamond', Georgia, 'Times New Roman', serif;
    padding: 2.5em 1.5em 4em;
    border-top: 4px double #8b5a2b;
    border-bottom: 4px double #8b5a2b;
  }
  .vm-wrap { max-width: 1200px; margin: 0 auto; }

  .vm-title {
    font-family: 'UnifrakturCook', 'Cormorant Garamond', Georgia, serif;
    font-size: 3em;
    text-align: center;
    color: #4a2e0e;
    margin: 0 0 0.1em;
    letter-spacing: 0.04em;
    text-shadow: 1px 1px 0 rgba(0,0,0,0.06);
    font-weight: 700;
  }
  .vm-subtitle {
    text-align: center;
    font-style: italic;
    color: #6b4423;
    margin: 0 auto 1.2em;
    max-width: 720px;
    font-size: 1.15em;
  }
  .vm-divider {
    text-align: center;
    color: #8b5a2b;
    font-size: 1.6em;
    margin: 0.6em 0 2.5em;
    letter-spacing: 0.5em;
  }

  .vm-channel {
    margin-bottom: 3.2em;
    border-top: 2px solid #c9a872;
    border-bottom: 2px solid #c9a872;
    padding: 1.4em 0 1.6em;
    position: relative;
  }
  .vm-channel:first-of-type { border-top: none; padding-top: 0.3em; }

  .vm-channel-head {
    display: flex;
    align-items: center;
    gap: 1.1em;
    margin-bottom: 1.4em;
    padding-bottom: 0.8em;
    border-bottom: 1px solid rgba(139, 90, 43, 0.35);
  }
  .vm-channel-logo {
    width: 76px;
    height: 76px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #8b5a2b;
    box-shadow:
      0 0 0 1px #f4ecd8 inset,
      0 2px 6px rgba(74, 46, 14, 0.35);
    flex-shrink: 0;
    background: #f4ecd8;
  }
  .vm-channel-info { flex: 1; min-width: 0; }
  .vm-channel-name {
    font-size: 1.85em;
    font-weight: 700;
    color: #4a2e0e;
    margin: 0;
    line-height: 1.1;
    font-family: 'Cormorant Garamond', Georgia, serif;
    letter-spacing: 0.01em;
  }
  .vm-channel-name::before {
    content: "❦ ";
    color: #b87333;
    font-size: 0.85em;
  }
  .vm-channel-count {
    font-size: 0.95em;
    color: #6b4423;
    font-style: italic;
    margin-top: 0.15em;
  }

  .vm-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
    gap: 1.4em;
  }

  .vm-card {
    display: block;
    text-decoration: none;
    color: inherit;
    background: #fbf6e9;
    border: 1px solid #c9a872;
    border-radius: 3px;
    overflow: hidden;
    box-shadow:
      0 1px 0 rgba(255,255,255,0.6) inset,
      0 2px 6px rgba(74, 46, 14, 0.18);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    position: relative;
  }
  .vm-card:hover {
    transform: translateY(-2px);
    box-shadow:
      0 1px 0 rgba(255,255,255,0.6) inset,
      0 5px 14px rgba(74, 46, 14, 0.32);
  }
  .vm-thumb-wrap {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #2a1a08;
    overflow: hidden;
  }
  .vm-thumb {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
  .vm-play {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 54px; height: 54px;
    border-radius: 50%;
    background: rgba(184, 115, 51, 0.92);
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 0 3px rgba(244, 236, 216, 0.85);
    pointer-events: none;
    transition: transform 0.15s;
  }
  .vm-card:hover .vm-play { transform: translate(-50%, -50%) scale(1.1); }
  .vm-play::after {
    content: "";
    width: 0; height: 0;
    border-left: 14px solid #fbf6e9;
    border-top: 9px solid transparent;
    border-bottom: 9px solid transparent;
    margin-left: 4px;
  }
  .vm-card-body {
    padding: 0.8em 1em 1em;
  }
  .vm-card-date {
    font-size: 0.82em;
    color: #8b5a2b;
    font-style: italic;
    margin-bottom: 0.35em;
    letter-spacing: 0.03em;
  }
  .vm-card-title {
    font-weight: 600;
    font-size: 1em;
    line-height: 1.35;
    color: #3a2410;
  }
  .vm-more {
    margin-top: 0.9em;
    font-size: 0.92em;
    color: #6b4423;
    font-style: italic;
    text-align: right;
  }

  @media (max-width: 600px) {
    .vm-title { font-size: 2.2em; }
    .vm-channel-logo { width: 60px; height: 60px; }
    .vm-channel-name { font-size: 1.4em; }
    .vm-page { padding: 1.5em 0.8em 2.5em; }
  }
</style>

<a href="{{ '/' | relative_url }}">
  <img src="{{ '/assets/bannerheraldo.png' | relative_url }}" alt="Cabecera El Heraldo del Viejo Mundo" style="width:100%; height:auto; max-height:240px; object-fit:contain; display:block; margin-bottom: 1.5em;">
</a>

<div class="vm-page">
<div class="vm-wrap">

<h1 class="vm-title">La Cámara de los Heraldos</h1>
<p class="vm-subtitle">
  Crónicas en imagen de los <em>scriptoria</em> de la comunidad española dedicados al <strong>Viejo Mundo</strong> y a los <strong>juegos clásicos de Warhammer Fantasy</strong>.
</p>
<div class="vm-divider">⚜ &nbsp; ❦ &nbsp; ⚜</div>

{%- comment -%}
  Cada item: "Nombre del canal::slug-del-logo"
  El slug debe coincidir con assets/canales/<slug>.jpg
{%- endcomment -%}
{%- assign whitelist_raw = "La Forja del Fénix::la-forja-del-fenix|La Alianza del Viejo Mundo::la-alianza-del-viejo-mundo|13th Warrior::13th-warrior|Moria Wargames::moria-wargames|La Taberna del Enano::la-taberna-del-enano|La Taberna del Guerrero::la-taberna-del-guerrero|La Posada del Martillo::la-posada-del-martillo|Juegos y Dados::juegos-y-dados|Leyendas en Miniatura::leyendas-en-miniatura|La Escotilla Estaliana Podcast::la-escotilla-estaliana-podcast|Legión del Turia::legion-del-turia|Las arenas de Nehekhara::las-arenas-de-nehekhara|Pícnic en Drakenhof::picnic-en-drakenhof" | split: "|" -%}

{%- assign sorted_videos = site.videos | sort: "date" | reverse -%}

{%- for entry in whitelist_raw -%}
  {%- assign parts = entry | split: "::" -%}
  {%- assign canal = parts[0] -%}
  {%- assign slug = parts[1] -%}
  {%- assign canal_lower = canal | downcase -%}

  {%- assign canal_videos = "" | split: "" -%}
  {%- for v in sorted_videos -%}
    {%- assign v_canal = v.channel | downcase -%}
    {%- if v_canal == canal_lower -%}
      {%- assign canal_videos = canal_videos | push: v -%}
    {%- endif -%}
  {%- endfor -%}

  {%- if canal_videos.size > 0 -%}

  <section class="vm-channel">
    <div class="vm-channel-head">
      <img class="vm-channel-logo" src="{{ '/assets/canales/' | append: slug | append: '.jpg' | relative_url }}" alt="Logo de {{ canal }}" loading="lazy">
      <div class="vm-channel-info">
        <h2 class="vm-channel-name">{{ canal }}</h2>
        <div class="vm-channel-count">
          {{ canal_videos.size }} crónica{% if canal_videos.size != 1 %}s{% endif %} en el archivo
        </div>
      </div>
    </div>

    <div class="vm-grid">
      {%- for v in canal_videos limit: 8 -%}
      <a class="vm-card" href="{{ v.url | relative_url }}">
        <div class="vm-thumb-wrap">
          {%- if v.thumbnail -%}
          <img class="vm-thumb" src="{{ v.thumbnail }}" alt="{{ v.title | escape }}" loading="lazy">
          {%- endif -%}
          <div class="vm-play"></div>
        </div>
        <div class="vm-card-body">
          <div class="vm-card-date">{{ v.date | date: "%d de %B de %Y" | replace: "January", "enero" | replace: "February", "febrero" | replace: "March", "marzo" | replace: "April", "abril" | replace: "May", "mayo" | replace: "June", "junio" | replace: "July", "julio" | replace: "August", "agosto" | replace: "September", "septiembre" | replace: "October", "octubre" | replace: "November", "noviembre" | replace: "December", "diciembre" }}</div>
          <div class="vm-card-title">
            {{ v.title | remove: "Nuevo vídeo de " | remove: canal | remove: ": " | strip | truncate: 95 }}
          </div>
        </div>
      </a>
      {%- endfor -%}
    </div>

    {%- if canal_videos.size > 8 -%}
    <p class="vm-more">… y {{ canal_videos.size | minus: 8 }} más en el archivo del canal.</p>
    {%- endif -%}
  </section>

  {%- endif -%}
{%- endfor -%}

<div class="vm-divider" style="margin-top: 2.5em; margin-bottom: 0;">⚜ &nbsp; ❦ &nbsp; ⚜</div>

</div>
</div>
