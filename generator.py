import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension


# Input directory / file
TEMPLATE_DIR = '_templates'
CONTENT_DIR = '_content'
GLOBAL_DATA_DIR = '_data'

# Output directory
OUTPUT_DIR = 'public'

# Layout / Templates
DEFAULT_LAYOUT = 'base.html'

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    extensions=[MarkdownExtension],
)


def load_markdown_data(md_json_path):
    md_json_path = "{}.json".format(md_json_path.rstrip(".md"))
    if os.path.exists(md_json_path):
        with open(md_json_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}

def load_global_data():
    # Get all json files from the content directory
    json_files = [f for f in os.listdir(GLOBAL_DATA_DIR) if f.endswith('.json')]
    global_data_dict = {}

    for json_file in json_files:
        json_path = os.path.join(GLOBAL_DATA_DIR, json_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            global_data_dict[json_file.strip(".json")] = json.load(f)

    return global_data_dict

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def render_string(md_content, context):
    template = env.from_string(md_content)
    return template.render(context)

def load_data(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        frontmatter_data = frontmatter.load(f)
        markdown_data_dict = load_markdown_data(markdown_file)
    return frontmatter_data, markdown_data_dict

def get_final_out_path(out_path):
    if out_path.endswith('index.md'):
        return f"{os.path.splitext(out_path)[0]}.html"
    else:
        return os.path.join(os.path.splitext(out_path)[0], "index.html")

def write_to_file(final_out_path, layout, html_content, context):
    with open(final_out_path, 'w', encoding='utf-8') as f:
        context.pop('content')
        f.write(render_template(layout, {'content': html_content, **context }))

def process_markdown():
    markdown_files = glob.glob(os.path.join(CONTENT_DIR, "**/*.md"), recursive=True)
    global_data_dict = load_global_data()

    for markdown_file in markdown_files:
        frontmatter_data, markdown_data_dict = load_data(markdown_file)
        context = {**global_data_dict, **markdown_data_dict, **frontmatter_data.to_dict()}

        layout = frontmatter_data.get('layout', DEFAULT_LAYOUT)
        permalink = frontmatter_data.get('permalink')

        html_content = render_string(frontmatter_data.content, context)

        if permalink:
            permalink = render_string(permalink, context)
            out_path = os.path.join(OUTPUT_DIR, permalink)
        else:
            markdown_file.replace(CONTENT_DIR, OUTPUT_DIR)

        out_dir_name = os.path.splitext(out_path)[0]
        os.makedirs(out_dir_name, exist_ok=True)

        final_out_path = get_final_out_path(out_path)

        write_to_file(final_out_path, layout, html_content, context)



def generate_static_site():
    process_markdown()


if __name__ == '__main__':
    generate_static_site()
