---
layout: base.html
title: "All Tags"
---

<h1>{{ title }}</h1>

<p class="tag-container">Tags: {% for tag in collections.all_tags %}
  <a class="tags" href="/tags/{{ tag }}/">{{ tag }}</a>
  {% endfor %}
</p>


