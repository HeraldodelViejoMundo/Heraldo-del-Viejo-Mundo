---
layout: default
title: El Heraldo del Viejo Mundo
---

## Últimas noticias de *The Old World*

{% for post in site.posts limit:10 %}
### [{{ post.title }}]({{ post.url | relative_url }})
<small>{{ post.date | date: "%d /%m/%Y" }}</small>

{{ post.excerpt }}

---

{% endfor %}
