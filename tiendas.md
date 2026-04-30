---
layout: default
title: Tiendas
permalink: /tiendas/
---

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css">

<style>
  .tn-page {
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
  .tn-wrap { max-width: 1200px; margin: 0 auto; }

  .tn-title {
    font-family: 'UnifrakturCook', 'Cormorant Garamond', Georgia, serif;
    font-size: 3em;
    text-align: center;
    color: #4a2e0e;
    margin: 0 0 0.1em;
    letter-spacing: 0.04em;
    font-weight: 700;
  }
  .tn-subtitle {
    text-align: center;
    font-style: italic;
    color: #6b4423;
    margin: 0 auto 1em;
    max-width: 720px;
    font-size: 1.15em;
  }
  .tn-divider {
    text-align: center;
    color: #8b5a2b;
    font-size: 1.5em;
    margin: 0.4em 0 2em;
    letter-spacing: 0.5em;
  }
  .tn-disclaimer {
    text-align: center;
    font-size: 0.92em;
    font-style: italic;
    color: #6b4423;
    background: rgba(201, 168, 114, 0.18);
    border-left: 3px solid #b87333;
    border-right: 3px solid #b87333;
    padding: 0.8em 1.2em;
    margin: 0 auto 2em;
    max-width: 760px;
  }

  /* Mapa */
  #tn-map {
    height: 480px;
    border: 3px solid #8b5a2b;
    border-radius: 3px;
    box-shadow: 0 4px 12px rgba(74, 46, 14, 0.25);
    margin-bottom: 1.5em;
    background: #fbf6e9;
  }

  /* Filtros */
  .tn-filters {
    background: #fbf6e9;
    border: 1px solid #c9a872;
    border-radius: 3px;
    padding: 1em 1.2em;
    margin-bottom: 1.5em;
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    align-items: center;
    box-shadow: 0 1px 3px rgba(74, 46, 14, 0.12);
  }
  .tn-filters label {
    font-weight: 600;
    color: #4a2e0e;
    font-size: 0.95em;
  }
  .tn-filters select,
  .tn-filters input[type="text"] {
    padding: 0.45em 0.7em;
    border: 1px solid #8b5a2b;
    border-radius: 3px;
    background: #f4ecd8;
    font-family: inherit;
    font-size: 1em;
    color: #3a2410;
    min-width: 200px;
  }
  .tn-filters select:focus,
  .tn-filters input[type="text"]:focus {
    outline: 2px solid #b87333;
    outline-offset: 1px;
  }
  .tn-filter-group {
    display: flex;
    align-items: center;
    gap: 0.5em;
  }
  .tn-checks { display: flex; gap: 1em; flex-wrap: wrap; }
  .tn-checks label { font-weight: 500; cursor: pointer; user-select: none; }
  .tn-checks input { margin-right: 0.3em; vertical-align: middle; }
  .tn-count {
    margin-left: auto;
    font-style: italic;
    color: #6b4423;
    font-size: 0.95em;
  }

  /* Listado */
  .tn-province {
    margin-bottom: 2.5em;
  }
  .tn-province-head {
    font-size: 1.5em;
    font-weight: 700;
    color: #4a2e0e;
    margin: 0 0 0.6em;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #c9a872;
    font-family: 'Cormorant Garamond', Georgia, serif;
  }
  .tn-province-head::before {
    content: "❦ ";
    color: #b87333;
    font-size: 0.85em;
  }
  .tn-province-ccaa {
    font-size: 0.7em;
    font-weight: 400;
    color: #8b5a2b;
    font-style: italic;
    margin-left: 0.5em;
  }

  .tn-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
    gap: 1em;
  }

  .tn-card {
    background: #fbf6e9;
    border: 1px solid #c9a872;
    border-left: 5px solid #8b5a2b;
    border-radius: 3px;
    padding: 0.9em 1em;
    box-shadow: 0 1px 3px rgba(74, 46, 14, 0.12);
    transition: transform 0.12s, box-shadow 0.12s;
  }
  .tn-card.tn-gw {
    border-left-color: #a02020;
    background: linear-gradient(to right, rgba(160, 32, 32, 0.06), #fbf6e9 30%);
  }
  .tn-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 3px 8px rgba(74, 46, 14, 0.22);
  }
  .tn-card-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.5em;
    margin-bottom: 0.3em;
  }
  .tn-card-name {
    font-weight: 700;
    font-size: 1.08em;
    color: #3a2410;
    line-height: 1.25;
  }
  .tn-badge {
    flex-shrink: 0;
    font-size: 0.7em;
    font-weight: 700;
    padding: 0.2em 0.55em;
    border-radius: 2px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .tn-badge-gw { background: #a02020; color: #fbf6e9; }
  .tn-badge-ind { background: #8b5a2b; color: #fbf6e9; }
  .tn-card-chain {
    font-size: 0.85em;
    color: #8b5a2b;
    font-style: italic;
    margin-bottom: 0.3em;
  }
  .tn-card-addr {
    font-size: 0.92em;
    color: #4a2e0e;
    margin-bottom: 0.4em;
  }
  .tn-card-meta {
    font-size: 0.85em;
    color: #6b4423;
    line-height: 1.5;
  }
  .tn-card-meta a {
    color: #8b5a2b;
    text-decoration: underline;
    text-decoration-style: dotted;
  }
  .tn-card-meta a:hover { color: #a02020; }
  .tn-card-notes {
    font-size: 0.82em;
    color: #6b4423;
    font-style: italic;
    margin-top: 0.4em;
    padding-top: 0.4em;
    border-top: 1px dashed rgba(139, 90, 43, 0.4);
  }

  /* Popup en mapa */
  .leaflet-popup-content-wrapper {
    background: #fbf6e9;
    color: #3a2410;
    border: 2px solid #8b5a2b;
    border-radius: 3px;
    font-family: 'Cormorant Garamond', Georgia, serif;
  }
  .leaflet-popup-tip { background: #8b5a2b; }
  .tn-popup-name { font-weight: 700; font-size: 1.1em; margin-bottom: 0.2em; }
  .tn-popup-addr { font-size: 0.92em; margin-bottom: 0.3em; }
  .tn-popup-meta { font-size: 0.85em; }

  /* Iconos personalizados */
  .tn-marker-icon {
    border-radius: 50%;
    border: 2px solid #fbf6e9;
    box-shadow: 0 1px 4px rgba(0,0,0,0.45);
  }
  .tn-marker-gw { background: #a02020; }
  .tn-marker-ind { background: #8b5a2b; }

  .tn-empty {
    text-align: center;
    padding: 3em 1em;
    color: #6b4423;
    font-style: italic;
    font-size: 1.1em;
  }

  @media (max-width: 600px) {
    .tn-title { font-size: 2.2em; }
    #tn-map { height: 360px; }
    .tn-page { padding: 1.5em 0.8em 2.5em; }
    .tn-filters select, .tn-filters input[type="text"] { min-width: 140px; flex: 1; }
    .tn-count { width: 100%; margin-left: 0; }
  }
</style>

<a href="{{ '/' | relative_url }}">
  <img src="{{ '/assets/bannerheraldo.png' | relative_url }}" alt="Cabecera El Heraldo del Viejo Mundo" style="width:100%; height:auto; max-height:240px; object-fit:contain; display:block; margin-bottom: 1.5em;">
</a>

<div class="tn-page">
<div class="tn-wrap">

<h1 class="tn-title">El Mapa de los Mercaderes</h1>
<p class="tn-subtitle">
  Directorio de tiendas con distribución oficial de <em>Games Workshop</em> en España: tiendas oficiales <strong>Warhammer</strong>, cadenas independientes y comercios locales del hobby.
</p>
<div class="tn-divider">⚜ &nbsp; ❦ &nbsp; ⚜</div>

<div class="tn-disclaimer">
  Última actualización: <strong>abril de 2026</strong>. Los datos pueden variar; conviene confirmar horarios y dirección antes de desplazarse. ¿Falta tu tienda o hay algún error? <a href="mailto:contacto@elheraldodelviejomundo.com" style="color:#8b5a2b;">Avísanos</a>.
</div>

<div id="tn-map"></div>

<div class="tn-filters">
  <div class="tn-filter-group">
    <label for="tn-province">Provincia:</label>
    <select id="tn-province"><option value="">Todas</option></select>
  </div>
  <div class="tn-filter-group">
    <label for="tn-search">Buscar:</label>
    <input type="text" id="tn-search" placeholder="Nombre, calle, ciudad…">
  </div>
  <div class="tn-checks">
    <label><input type="checkbox" id="tn-gw" checked> Oficiales GW</label>
    <label><input type="checkbox" id="tn-ind" checked> Independientes</label>
  </div>
  <div class="tn-count" id="tn-count">Cargando…</div>
</div>

<div id="tn-list"></div>

<div class="tn-divider" style="margin-top: 2.5em; margin-bottom: 0;">⚜ &nbsp; ❦ &nbsp; ⚜</div>

</div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<script>
(function(){
  const DATA_URL = "{{ '/assets/data/tiendas.json' | relative_url }}";
  const $province = document.getElementById('tn-province');
  const $search   = document.getElementById('tn-search');
  const $gw       = document.getElementById('tn-gw');
  const $ind      = document.getElementById('tn-ind');
  const $count    = document.getElementById('tn-count');
  const $list     = document.getElementById('tn-list');

  // Mapa centrado en España
  const map = L.map('tn-map', { scrollWheelZoom: false }).setView([40.0, -3.5], 6);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(map);
  // Activar zoom por rueda al hacer clic dentro
  map.on('focus', () => map.scrollWheelZoom.enable());
  map.on('blur',  () => map.scrollWheelZoom.disable());

  const cluster = L.markerClusterGroup({ maxClusterRadius: 50 });
  map.addLayer(cluster);

  function makeIcon(kind) {
    const cls = kind === 'GW' ? 'tn-marker-gw' : 'tn-marker-ind';
    return L.divIcon({
      className: 'tn-marker-icon ' + cls,
      iconSize: [16, 16],
      html: ''
    });
  }

  function escapeHtml(s) {
    if (!s) return '';
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function popupHtml(s) {
    let html = '<div class="tn-popup-name">' + escapeHtml(s.name) + '</div>';
    if (s.chain) html += '<div style="font-style:italic;color:#8b5a2b;font-size:0.85em;margin-bottom:0.3em;">Parte de ' + escapeHtml(s.chain) + '</div>';
    html += '<div class="tn-popup-addr">' + escapeHtml(s.address) + '</div>';
    let meta = [];
    if (s.phone) meta.push('☎ ' + escapeHtml(s.phone));
    if (s.web) {
      let web = s.web.startsWith('http') ? s.web : 'https://' + s.web;
      meta.push('<a href="' + escapeHtml(web) + '" target="_blank" rel="noopener">' + escapeHtml(s.web) + '</a>');
    }
    if (meta.length) html += '<div class="tn-popup-meta">' + meta.join(' · ') + '</div>';
    return html;
  }

  function cardHtml(s) {
    const kindCls = s.kind === 'GW' ? 'tn-gw' : 'tn-ind';
    const badgeCls = s.kind === 'GW' ? 'tn-badge-gw' : 'tn-badge-ind';
    const badgeTxt = s.kind === 'GW' ? 'Oficial GW' : 'Independiente';
    let html = '<div class="tn-card ' + kindCls + '">';
    html += '<div class="tn-card-head">';
    html += '  <div class="tn-card-name">' + escapeHtml(s.name) + '</div>';
    html += '  <span class="tn-badge ' + badgeCls + '">' + badgeTxt + '</span>';
    html += '</div>';
    if (s.chain) html += '<div class="tn-card-chain">Parte de ' + escapeHtml(s.chain) + '</div>';
    html += '<div class="tn-card-addr">📍 ' + escapeHtml(s.address) + '</div>';
    let meta = [];
    if (s.phone) meta.push('☎ ' + escapeHtml(s.phone));
    if (s.web) {
      let web = s.web.startsWith('http') ? s.web : 'https://' + s.web;
      meta.push('🔗 <a href="' + escapeHtml(web) + '" target="_blank" rel="noopener">' + escapeHtml(s.web) + '</a>');
    }
    if (s.email) meta.push('✉ <a href="mailto:' + escapeHtml(s.email) + '">' + escapeHtml(s.email) + '</a>');
    if (meta.length) html += '<div class="tn-card-meta">' + meta.join(' · ') + '</div>';
    if (s.notes) html += '<div class="tn-card-notes">' + escapeHtml(s.notes) + '</div>';
    html += '</div>';
    return html;
  }

  function strip(s) {
    return (s || '').toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  let allShops = [];

  function render() {
    const prov = $province.value;
    const q = strip($search.value.trim());
    const showGw = $gw.checked;
    const showInd = $ind.checked;

    const filtered = allShops.filter(s => {
      if (!showGw && s.kind === 'GW') return false;
      if (!showInd && s.kind === 'IND') return false;
      if (prov && s.province !== prov) return false;
      if (q) {
        const blob = strip(s.name + ' ' + s.address + ' ' + (s.chain || '') + ' ' + s.province + ' ' + s.ccaa);
        if (!blob.includes(q)) return false;
      }
      return true;
    });

    // Mapa: limpiar y rellenar
    cluster.clearLayers();
    filtered.forEach(s => {
      const m = L.marker([s.lat, s.lon], { icon: makeIcon(s.kind) });
      m.bindPopup(popupHtml(s));
      cluster.addLayer(m);
    });

    // Centrar mapa según filtro
    if (prov && filtered.length > 0) {
      const group = L.featureGroup(cluster.getLayers());
      try { map.fitBounds(group.getBounds().pad(0.2)); } catch(e) {}
    } else if (!prov) {
      map.setView([40.0, -3.5], 6);
    }

    // Listado: agrupar por provincia
    if (filtered.length === 0) {
      $list.innerHTML = '<div class="tn-empty">No se han encontrado tiendas con esos filtros.</div>';
    } else {
      const byProv = {};
      filtered.forEach(s => {
        const k = s.province;
        if (!byProv[k]) byProv[k] = { ccaa: s.ccaa, shops: [] };
        byProv[k].shops.push(s);
      });
      const sortedProvs = Object.keys(byProv).sort((a,b) => a.localeCompare(b, 'es'));
      let html = '';
      sortedProvs.forEach(p => {
        const grp = byProv[p];
        html += '<section class="tn-province">';
        html += '<h2 class="tn-province-head">' + escapeHtml(p);
        html += '<span class="tn-province-ccaa">— ' + escapeHtml(grp.ccaa) + '</span>';
        html += '</h2>';
        html += '<div class="tn-grid">';
        grp.shops.forEach(s => { html += cardHtml(s); });
        html += '</div></section>';
      });
      $list.innerHTML = html;
    }

    const total = allShops.length;
    $count.textContent = filtered.length === total
      ? `${total} tiendas`
      : `${filtered.length} de ${total} tiendas`;
  }

  fetch(DATA_URL)
    .then(r => r.json())
    .then(data => {
      allShops = data;
      // Provincias únicas
      const provs = [...new Set(data.map(s => s.province))].sort((a,b) => a.localeCompare(b, 'es'));
      provs.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p; opt.textContent = p;
        $province.appendChild(opt);
      });
      render();
    })
    .catch(e => {
      $count.textContent = 'Error al cargar el directorio';
      $list.innerHTML = '<div class="tn-empty">No se ha podido cargar el directorio. Inténtalo de nuevo más tarde.</div>';
      console.error(e);
    });

  $province.addEventListener('change', render);
  $search.addEventListener('input', render);
  $gw.addEventListener('change', render);
  $ind.addEventListener('change', render);
})();
</script>
