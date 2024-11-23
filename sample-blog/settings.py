
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
STATIC_PATHS = [
    "images", #whole directory
    "assets/robots.txt" #specific file
]

# Define plugin folders to copy, if they exist
PLUGIN_LOOKUP_FOLDERS = ["templates", "static"]

# List of plugin modules to load
PLUGIN_MODULES = ['myplugins']

PAGE_SIZE = 10

SITE_NAME = 'https://pyjan26.dev'
SITEMAP_CONFIG = [
    { 'collection': CONTENT_DIR, 'changefreq': 'monthly', 'priority': 0.8 },
    { 'collection': 'posts', 'changefreq': 'monthly', 'priority': 0.8 },
    { 'collection': 'tags', 'changefreq': 'monthly', 'priority': 0.8 },
]


