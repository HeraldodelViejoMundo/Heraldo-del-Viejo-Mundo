---
layout: default
title: El Heraldo del Viejo Mundo
---

## Últimas noticias de *The Old World*

{% for post in site.posts limit:10 %}
### <a href="{{ post.url | relative_url }}"><span style="color:#000;font-weight:700;font-size:0.7em">Hoy en Warhammer Community:</span> <span style="color:#0057b8">{{ post.title_original }}</span> <span style="color:#555;font-size:0.8em">({{ post.title_translated }})</span></a>


<small>{{ post.date | date: "%d /%m/%Y" }}</small>

{{ post.excerpt }}

---

{% endfor %}
