---
layout: default
title: El Heraldo del Viejo Mundo
---

## Últimas noticias de *The Old World*

{% for post in site.posts limit:20 %}
### <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
<small>{{ post.date | date: "%d/%m/%Y" }}</small>

{% if post.thumbnail %}
<img src="{{ post.thumbnail }}" alt="Miniatura del vídeo" style="width:60%; max-width:300px; margin:10px 0;">
{% endif %}

{% if post.image %}
<img src="{{ post.image }}" alt="Imagen del artículo" style="width:100%; max-width:500px; margin:10px 0;">
{% endif %}

{{ post.excerpt }}
---
{% endfor %}
