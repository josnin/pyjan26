
# Input directory / file
TEMPLATE_DIR = 'templates'
CONTENT_DIR = 'content'

# Output directory
OUTPUT_DIR = 'public'

# Layout / Templates
DEFAULT_LAYOUT = 'base.html'


# Copy Static files
STATIC_PATHS = [
    "images",
    "*/robots.txt"
]


METADATA = {
    "abc": "efg"
}

DATA = {
  "title": "My Static Site",
  "author": "John Doe",
  "description": "A simple static site generated with Python and Jinja2."
}