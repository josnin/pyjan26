# PyJan26
PyJan26 is a static site generator written in Python. It allows you to generate static websites from templates and content files, with support for pagination, and extend using plugins.

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
layout: base.html   # Specify the layout template
title: Blog Post 1                  # Set the title of the page
paginated:                     # Configure pagination
  data: blogs                  # Specify the collections 
  size: 10                      # Set the number of items per page
  alias: myblogs                # Set a custom alias for the paginated items
```

### Pagination Variables
When pagination is enabled, PyJan26 provides built-in template variables that you can use to generate pagination links:

```html
{% if myblogs %}
  {% for post in myblogs %}
    <span><a href="/posts/{{ post.name }}/">{{ post.name }}</a></span>
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
```

In this example:

* myblogs represents the paginated blogs.
* pagination.total_pages represents the total pages.
* pagination.prev_page provides a link to the previous page.
* pagination.page_number represents the current page number.
* pagination.page_numbers generates links to each page.
* pagination.next_page provides a link to the next page.


## Copy Static Files
To specify static files to be copied to the public directory, add them to the STATIC_PATH_PATTERNS variable in your configuration (settings.py):

can make use of Wildcards available in glob()
```python
STATIC_PATH_PATTERNS = [
    "assets/*.css",
]
```

Adjust the paths as needed to include directories or specific files you want to copy.

# Extending Functionality Using Plugins

To extend the functionality of your site, follow these steps to use plugins:

1. Install the Plugin
Install the plugin using pip:

```python
pip install <plugin-name>
```

Alternatively, include your plugin as a Python module in your project.

2. Register the Plugin Module in settings.py
Add the plugin module to the PLUGIN_MODULES list in your settings:

```python
PLUGIN_MODULES = ['myplugins']
```

Add or Replace 'myplugins' with the name of your plugin module

3. Copy templates/static plugin files
To copy templates or static files provided by a plugin, run the following command

```bash
python -m pyjan26.main c
```

## Creating Your Own Plugin
To create your own plugin, follow these steps

1. Register Custom Features
Add custom functionality 

#### Custom Collections
Define custom collections in my_custom_plugin.py:

```python
from pyjan26.registry import register_custom_collections

def blog_collections(collections):
    return {'blogs': list(filter(lambda post: post['name'] != 'index', collections.get('posts'))) }

def all_tags_collections(collections):
    #depdent on blog_collections
    return {'all_tags': list(tag for blog in collections.get('blogs') for tag in blog['tags'])}

register_custom_collections([
    blog_collections,
    all_tags_collections
])
```

#### Custom Filters
Define custom filters in the same file my_custom_plugin.py:

```python

from pyjan26.registry import register_custom_filters

def capitalize_words(value):
    return ' '.join(word.capitalize() for word in value.split())


# Register custom filters
register_custom_filters([capitalize_words])
```

To use the custom filter in your templates, follow this syntax:
```python
{{ content | capitalize_words }}
```

#### Custom Page Rendering
Define custom page rendering in the same file my_custom_plugin.py:

```python
from pyjan26.registry import register_custom_pages
from pyjan26.core import render_page

### START Custom Page #########
def repeat_page(*args, **kwargs):
    item, collection_name, collections, settings, permalink = args
    for data1 in collections.get(item.get('data')):
        item['page_items'] = data1
        page_data = {
            'collection_name': collection_name, 
            'collections': collections,  
            'settings': settings, 
            'items': item,
            'permalink2': f'{data1}/'
        }
        render_page(page_data)

    return { 'skip_next': True }

register_custom_pages([repeat_page])

```

To apply custom page rendering to a content markdown file, add repeat_page: True to the YAML front matter:

```yaml
---
layout: base.html
repeat_page: True #Apply custom page rendering
data: all_tags
title: mytitle
---
```

This instructs PyJan26 to use the repeat_page function for rendering this specific content. Adjust metadata as needed.

2. Include Templates and Static Files (if require)
To package templates and static files within your plugin:
* Ensure your plugin has the required files in appropriate directories(templates, static, etc.)
* Update your setup.py to include these files

3. Example setup.py:
```python
from setuptools import setup, find_packages

setup(
    name="my_custom_plugin",
    version="1.0.0",
    packages=find_packages(),
    package_data={
	"my_custom_plugin": ["templates/*", "static/*"] #Include templates and static files
    }
)
```

This will include your templates and static folders in the plugin package


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

## How to run development server?

```bash
git clone https://github.com/josnin/pyjan26.git
cd ~/Documents/pyjan26/
```

## Help

Need help? Open an issue in: [ISSUES](https://github.com/josnin/pyjan26/issues)


## Contributing
Want to improve and add feature? Fork the repo, add your changes and send a pull request.
