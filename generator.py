import os
import json
import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader
from jinja2_markdown import MarkdownExtension

# Set up Jinja2 environment
template_dir = 'input/templates'
env = Environment(
    loader=FileSystemLoader(template_dir),
    extensions=[MarkdownExtension],
)

# Output directory
output_dir = 'output'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def load_from_md_json(md_json_path):
    md_json_path = "{}.json".format(md_json_path)
    if os.path.exists(md_json_path):
        with open(md_json_path, 'r', encoding='utf-8') as json_file:
            print(md_json_path)
            return json.load(json_file)
    return {}

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def convert_markdown_to_html(md_content, context):
    template = env.from_string(md_content)
    return template.render(context)


def generate_static_site():
    # Get all markdown files from the content directory
    content_dir = 'input/content'
    markdown_files = [f for f in os.listdir(content_dir) if f.endswith('.md')]

    for markdown_file in markdown_files:
        # Read the markdown content along with front matter
        md_path = os.path.join(content_dir, markdown_file)
        with open(os.path.join(content_dir, markdown_file), 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            data_md_json = load_from_md_json(md_path)

        # Extract layout information from front matter or use a default layout
        layout = post.get('layout', 'base.html')

        print(data_md_json)

        # Pass Jinja variables from front matter to the template
        context = { **post.to_dict(), **data_md_json }

        # Convert markdown to HTML, including Jinja variables
        html_content = convert_markdown_to_html(post.content, context)

        # Determine the output file path
        output_file_path = os.path.join(output_dir, os.path.splitext(markdown_file)[0] + '.html')

        # Render the specified layout template and write to the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(render_template(layout, {'content': html_content}))

if __name__ == '__main__':
    generate_static_site()
