from jinja2 import Environment, FileSystemLoader, BaseLoader, DebugUndefined
import markdown

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
    "assets", #whole directory
]

# Configuration for markdown
MARKDOWN_PROCESSOR = markdown.Markdown(
    extensions=[]
)

# Template Engine: Jinja2 by default (replaceable)
TEMPLATE_ENGINE = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    undefined=DebugUndefined
)

# Define plugin folders to copy, if they exist
PLUGIN_LOOKUP_FOLDERS = ["templates", "static"]

# List of plugin modules to load
PLUGIN_MODULES = []

# Default Pagination Size
PAGE_SIZE = 10



