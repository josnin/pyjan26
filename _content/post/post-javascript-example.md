---
layout: page.html
title: Post 1 page
tags: ["vue", "react"]
jump: True
split_by:
  items: collection2
  alias: blogPosts
out_dir: 'new/{{ title.replace(" ", "-") }}'
---

# Post1 page


{% for page in blogPosts %}
    <span>{{ page.url }}</span>
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





Im in Post1 page
