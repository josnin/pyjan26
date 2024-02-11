---
layout: page.html
title: Index Post
page_size: 2
paginated_items: post
---

# Index post


{% for page in paginatedPost %}
    <span>{{ page.layout }}</span>
{% endfor %}





Im index post