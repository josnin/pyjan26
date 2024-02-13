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


{% if pagination.prev_page %}
  <a href="{{ pagination.prev_page }}">Previous</a>
{% endif %}

{% for page_num in pagination.page_numbers %}
  <a href="/post/{{ page_num }}">{{ page_num }}</a>
{% endfor %}

{% if pagination.next_page %}
  <a href="{{ pagination.next_page }}">Next</a>
{% endif %}





Im index post