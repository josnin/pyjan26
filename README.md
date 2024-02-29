# PyJan26
PyJan26 is a static site generator written in Python. It allows you to generate static websites from templates and content files, with support for pagination, custom pages, custom filters, and custom collections.

## Install PyJan26 using pip:

```bash
pip install pyjan26
```

Initialize a new project:

```bash
python -m pyjan26.main s <project_name>
cd <project_name>
```

Generate static site:

```bash
python -m pyjan26.main g
```

To run your generated static site :

```bash
python -m http.server --directory public/
```

## Directory Structure

PyJan26 follows a specific directory structure:

```bash
project_directory/
│
├── _templates/          # Base and extendable templates
│   ├── base.html        
│   └── custom_template.html  
│
├── _content/            # Content files (Markdown)
│   ├── post1.md        
│   ├── post2.md        
│   └── about.md        

│
└── public/               # Generated HTML files
    ├── index.html      
    ├── post1/
    │   └── index.html   # Generated page for post1
    ├── post2/
    │   └── index.html   # Generated page for post2
    └── about/
        └── index.html   # Generated page for about

```

### Pagination

To configure pagination, add the following YAML front matter to your content files:

```yaml
layout: custom_template.html   # Specify the layout template
title: Post 1                  # Set the title of the page
paginated:                     # Configure pagination
  items: tags                  # Specify the grouping criteria / collections (e.g., tags)
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

* myitem represents the paginated items.
* pagination.prev_page provides a link to the previous page.
* pagination.page_numbers generates links to each page.
* pagination.next_page provides a link to the next page.


## Copy Static Files
To specify static files to be copied to the public directory, add them to the STATIC_PATHS variable in your configuration (settings.py):

```python
# Copy Static files
STATIC_PATHS = [
    "images",     # whole directory
    "assets/robots.txt"   # specific file
]
```
Adjust the paths as needed to include directories or specific files you want to copy.

## Customization
* Define custom collections in custom_collections.py.
* Define custom filters in custom_filters.py.
* Define custom page rendering in custom_pages.py.


## Global Variable

To create a global variable, simply define it in settings.py:

```python
# settings.py

#example only
AUTHOR = 'Josnin'
```

This renders the template value of AUTHOR defined in the settings.py module.

```html
{{ settings.AUTHOR }}
```

