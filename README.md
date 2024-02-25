# PyJan26
PyJan26 is a static site generator written in Python. It allows you to generate static websites from templates and content files, with support for pagination, custom pages, custom filters, and custom collections.

## Installation
You can install PyJan26 using pip:

```bash
pip install pyjan26
```

## Directory Structure

PyJan26 follows a specific directory structure:

project_directory/
│
├── _templates/ # Base and extendable templates
│ ├── base.html
│ └── custom_template.html
│
├── _content/ # Content files (Markdown)
│ ├── post1.md
│ ├── post2.md
│ └── about.md
│
└── public/ # Generated HTML files
├── index.html
├── post1/index.html
├── post2/index.html
└── about/index.html


### Usage

- **Templates**: Design your base and extendable templates in `_templates`.
- **Content**: Define content files in `_content`. Each file specifies the layout and content of a page.
- **Generated Files**: PyJan26 generates static HTML files in the `public` folder based on templates and content files.

### Pagination

To configure pagination, add the following YAML front matter to your content files:

```yaml
layout: custom_template.html   # Specify the layout template
title: Post 1                  # Set the title of the page
paginated:                     # Configure pagination
  items: tags                  # Specify the grouping criteria (e.g., tags)
  size: 1                      # Set the number of items per page
  alias: myitem                # Set a custom alias for the paginated items
```

### Pagination Variables
When pagination is enabled, PyJan26 provides built-in template variables that you can use to generate pagination links:

```html
{% if myitem %}
  {% for page in myitem %}
    <span><a href="/post/{{ page.tag }}">{{ page.tag }}</a></span>
  {% endfor %}
{% endif %}

{% if pagination.prev_page %}
  <a href="{{ pagination.prev_page }}">Previous</a>
{% endif %}

{% for page_num in pagination.page_numbers %}
  <a href="{{ page_num.url }}">{{ page_num.page_number }}</a>
{% endfor %}

{% if pagination.next_page %}
  <a href="{{ pagination.next_page }}">Next</a>
{% endif %}
```

In this example:

myitem represents the paginated items.
pagination.prev_page provides a link to the previous page.
pagination.page_numbers generates links to each page.
pagination.next_page provides a link to the next page.
