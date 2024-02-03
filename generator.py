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
    json_path = f"{os.path.splitext(md_json_path)[0]}.json"
    return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}

def load_global_data(global_data_dir):
    return {os.path.splitext(file)[0]: json.load(open(os.path.join(global_data_dir, file), 'r', encoding='utf-8'))
            for file in os.listdir(global_data_dir) if file.endswith('.json')}

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def render_string(md_content, context):
    template = env.from_string(md_content)
    return template.render(context)

def load_data(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        return frontmatter.load(f), load_markdown_data(markdown_file)

def get_final_out_path(out_path):
    base_path, extension = os.path.splitext(out_path)
    return f"{base_path}.html" if out_path.endswith('index.md') else os.path.join(base_path, "index.html")

def write_to_file(final_out_path, layout, html_content, context):
    with open(final_out_path, 'w', encoding='utf-8') as f:
        context.pop('content')
        f.write(render_template(layout, {'content': html_content, **context }))

def process_markdown():
    markdown_files = glob.glob(os.path.join(CONTENT_DIR, "**/*.md"), recursive=True)
    global_data_dict = load_global_data(GLOBAL_DATA_DIR)

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
            out_path = markdown_file.replace(CONTENT_DIR, OUTPUT_DIR)

        out_dir_name = os.path.splitext(out_path)[0]
        #TODO it also generates public/index folder
        os.makedirs(out_dir_name, exist_ok=True)
        print('makedirs', out_dir_name)

        final_out_path = get_final_out_path(out_path)
        print('write here', final_out_path)

        write_to_file(final_out_path, layout, html_content, context)



def generate_static_site():
    process_markdown()


if __name__ == '__main__':
    generate_static_site()
