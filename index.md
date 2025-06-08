---
layout: default
title: El Heraldo del Viejo Mundo
---

## Últimas noticias de *The Old World*

{% for post in site.posts limit:10 %}
### <a href="{{ post.url | relative_url }}"><span style="color:#000;font-weight:700;font-size:0.7em">Hoy, en Warhammer Community:</span> <span style="color:#0057b8">{{ post.title_translated }}</span></a>

<small>{{ post.date | date: "%d/%m/%Y" }}</small>

{% if post.image %}
<img src="{{ post.image }}" alt="Imagen del artículo" style="width:100%; max-width:500px; margin:10px 0;">
{% endif %}

{{ post.excerpt }}

---

{% endfor %}

