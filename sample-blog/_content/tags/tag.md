---
repeat_page: True
data: all_tags
title: mytitle
layout: base.html
permalink: '{{ tag }}'
---


<h2>Filtered by tag: {{ tag }}</h2>

<div class="pst-ctnr">
  {% for post in collections.blogs %}
    <div class="pst-ctnr__post">
      <h2 class="pst-ctnr__post__header"><a href="{{ post.url }}">{{ post.name }}</a></h2>
      <p class="pst-ctnr__post__desc">{{ post.description }}</p>
    </div>
  {% endfor %}
</div>



<p>See <a href="/tags/">all tags</a>.</p>
