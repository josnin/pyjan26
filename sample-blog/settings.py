from jinja2 import Environment, FileSystemLoader, BaseLoader, DebugUndefined
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

# Debugger
DEBUG = False

# Input directory / file
TEMPLATE_DIR = '_templates'
CONTENT_DIR = '_content'

# Output directory
OUTPUT_DIR = 'public'

# Layout / Templates
DEFAULT_LAYOUT = 'base.html'

# Copy Static files
# can make use of Wildcards available in glob()
STATIC_PATH_PATTERNS = [
    "assets/*.css",
]

# Configuration for markdown
MARKDOWN_PROCESSOR = markdown.Markdown(
    extensions=['fenced_code', CodeHiliteExtension(linenums=True)]
)

# Template Engine: Jinja2 by default (replaceable)
TEMPLATE_ENGINE = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    undefined=DebugUndefined
)

# Define plugin folders to copy, if they exist
PLUGIN_LOOKUP_FOLDERS = ["templates", "static"]

# List of plugin modules to load
PLUGIN_MODULES = [
    'plugins.blogs_w_tags',
    'plugins.repeat_page',
    'plugins.sitemap',
    'plugins.css_to_scss'
]

# Default Pagination Size
PAGE_SIZE = 10

SITE_NAME = 'https://pyjan26.dev'
SITEMAP_CONFIG = [
    { 'collection': CONTENT_DIR, 'changefreq': 'monthly', 'priority': 0.8 },
    { 'collection': 'posts', 'changefreq': 'monthly', 'priority': 0.8 },
    { 'collection': 'tags', 'changefreq': 'monthly', 'priority': 0.8 },
]

# Define scss files to convert to css
CSS_SCSS_PATTERNS = ['assets/*.scss']