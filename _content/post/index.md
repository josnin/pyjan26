---
layout: page.html
title: Index Post
---

# Index post

{% for page in collections.collection2 %}
    <span>{{ page.title }}</span>
{% endfor %}

{% for page in blogPosts %}
    <span>{{ page.title }}</span>
{% endfor %}


{% if pagination.prev_page %}
  <a href="{{ pagination.prev_page }}">Previous</a>
{% endif %}

{% for page_num in pagination.page_numbers %}
  <a href="{{ page_num.url }}">{{ page_num.page_number }}</a>
{% endfor %}

{% if pagination.next_page %}
  <a href="{{ pagination.next_page }}">Next</a>
{% endif %}





Im index post