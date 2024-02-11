---
layout: page.html
title: Index Post
---

# Index post

{{ collections.post }}

{% for page in paginatedPost %}
    <span>{{ page.layout }}</span>
{% endfor %}





Im index post