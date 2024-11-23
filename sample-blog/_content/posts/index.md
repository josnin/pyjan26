---
layout: base.html
paginated:
  data: blogs
  size: 1
  alias: myblogs
title: Technical Blogs | Share Insights, Tutorials, and Innovations
---

<p class="tag-container">Tags: {% for tag in collections.all_tags %}
  <a class="tags" href="/tags/{{ tag }}/">{{ tag }}</a>
  {% endfor %}
</p>

<div class="pst-ctnr">
  {% for post in myblogs %}
    <div class="pst-ctnr__post">
      <h2 class="pst-ctnr__post__header"><a href="{{ post.url }}">{{ post.name }}</a></h2>
      <p class="pst-ctnr__post__desc">{{ post.description }}</p>
    </div>
  {% endfor %}
</div>


{% if myblogs %}
  {% for blog in myblogs %}
    <span><a href="/blog/{{ blog.name }}">{{ blog.name }}</a></span>
  {% endfor %}
{% endif %}

{% if pagination.prev_page %}
  <a href="{{ pagination.prev_page }}">Previous</a>
{% endif %}

{% for page_num in pagination.page_numbers %}
  <a href="{{ page_num.url }}">{{ page_num.page_number }}</a>
{% endfor %}

{% if pagination.page_number and pagination.total_pages %}
  Page {{ pagination.page_number}} of: {{ pagination.total_pages }}
{% endif %}

{% if pagination.next_page %}
  <a href="{{ pagination.next_page }}">Next</a>
{% endif %}