---
sitemap_page: True
---
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {% for page in collections.sitemap %}
    <url>
      <loc>{{ page.loc }}</loc>
      <changefreq>{{ page.changefreq }}</changefreq>
      <priority>{{ page.priority }}</priority>
    </url>
  {% endfor %}
</urlset>