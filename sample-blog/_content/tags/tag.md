---
layout: base.html
repeat_page: True
data: all_tags
title: mytitle
---

<!-- page_items contains tag name. ex. Javascript -->
<h2>Filtered by tag: {{ page_items }}</h2>

<div class="pst-ctnr">
  {% for post in collections.blogs | filter_tag(page_items) %}
    <div class="pst-ctnr__post">
      <h2 class="pst-ctnr__post__header"><a href="/posts/{{ post.name }}/">{{ post.name }}</a></h2>
      <p class="pst-ctnr__post__desc">{{ post.description }}</p>
    </div>
  {% endfor %}
</div>



<p>See <a href="/tags/">all tags</a>.</p>
