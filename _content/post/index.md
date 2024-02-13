---
layout: page.html
title: Index Post
paginated:
  size: 1
  items: post
  alias: blogPosts
---

# Index post


{% for page in blogPosts %}
    <span>{{ page.url }}</span>
{% endfor %}





Im index post