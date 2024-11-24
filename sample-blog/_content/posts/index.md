---
layout: base.html
paginated:
  data: blogs
  size: 1
  alias: myblogs
title: Blog Posts
---

<p class="tag-container">Tags: {% for tag in collections.all_tags %}
  <a class="tags" href="/tags/{{ tag }}/">{{ tag }}</a>
  {% endfor %}
</p>

<div class="pst-ctnr">
  {% for post in myblogs %}
    <div class="pst-ctnr__post">
      <h2 class="pst-ctnr__post__header"><a href="/posts/{{post.name}}/">{{ post.name }}</a></h2>
      <p class="pst-ctnr__post__desc">{{ post.description }}</p>
    </div>
  {% endfor %}
</div>

<ul>
{% if pagination.prev_page %}
  <li><a href="{{ pagination.prev_page }}">Previous</a></li>
{% endif %}

{% for page_num in pagination.page_numbers %}
  <li><a  href="{{ page_num.url }}">{{ page_num.page_number }}</a></li>
{% endfor %}

{% if pagination.page_number and pagination.total_pages %}
  <li>Page {{ pagination.page_number}} of: {{ pagination.total_pages }}</li>
{% endif %}

{% if pagination.next_page %}
  <li><a href="{{ pagination.next_page }}">Next</a></li>
{% endif %}

</ul>