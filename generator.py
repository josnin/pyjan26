import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension


# Input directory / file
template_dir = 'input/templates'
content_dir = 'input/content'
global_data_dir = 'input/data'
default_layout = 'base.html'

# Output directory
output_dir = 'output'

# Set up Jinja2 environment
env = Environment(
    loader=FileSystemLoader(template_dir),
    extensions=[MarkdownExtension],
)


# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def load_markdown_data(md_json_path):
    md_json_path = "{}.json".format(md_json_path.rstrip(".md"))
    if os.path.exists(md_json_path):
        with open(md_json_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    return {}

def load_global_data():
    # Get all json files from the content directory
    json_files = [f for f in os.listdir(global_data_dir) if f.endswith('.json')]
    global_data_dict = {}

    for json_file in json_files:
        json_path = os.path.join(global_data_dir, json_file)
        with open(json_path, 'r', encoding='utf-8') as f:
            global_data_dict[json_file.strip(".json")] = json.load(f)

    return global_data_dict

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def render_string(md_content, context):
    template = env.from_string(md_content)
    return template.render(context)

def process_markdown():
    # Get all markdown files from the content directory
    markdown_files = glob.glob("{}/**/*.md".format(content_dir), recursive=True)

    global_data_dict = load_global_data()

    for markdown_file in markdown_files:
        # Read the markdown content along with front matter
        with open(markdown_file, 'r', encoding='utf-8') as f:
            frontmatter_data = frontmatter.load(f)
            markdown_data_dict = load_markdown_data(markdown_file)
        
        # Pass Jinja variables from front matter to the template , based on priority
        context = { **global_data_dict, **markdown_data_dict, **frontmatter_data.to_dict() }

        # Extract layout information from front matter or use a default layout
        layout = frontmatter_data.get('layout', default_layout)
        permalink = frontmatter_data.get('permalink', output_dir)

        # Convert markdown to HTML, including Jinja variables
        html_content = render_string(frontmatter_data.content, context)

        #Convert jinja variables in permalink
        permalink = render_string(permalink, context)

        out_path = markdown_file.replace(content_dir, permalink)
        out_dir_name = "{}".format(out_path.rstrip(".md"))
        os.makedirs(out_dir_name, exist_ok=True)
        print(f"Created output directory: {out_dir_name}")

        # Render the specified layout template and write to the output file
        # /output/posts/abc/index.html
        final_out_path = "{}/index.html".format(out_dir_name)
        with open(final_out_path, 'w', encoding='utf-8') as f:

            # rm content so it wont override the new content
            context.pop('content')

            f.write(render_template(layout, {'content': html_content, **context }))


def generate_static_site():
    process_markdown()


if __name__ == '__main__':
    generate_static_site()
