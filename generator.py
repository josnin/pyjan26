import os
import markdown2
from jinja2 import Environment, FileSystemLoader
import frontmatter

# Set up Jinja2 environment
template_dir = 'input/templates'
env = Environment(loader=FileSystemLoader(template_dir))

# Output directory
output_dir = 'output'

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def render_template(template_name, context):
    template = env.get_template(template_name)
    return template.render(context)

def convert_markdown_to_html(md_content):
    return markdown2.markdown(md_content)

def generate_static_site():
    # Get all markdown files from the content directory
    content_dir = 'input/content'
    markdown_files = [f for f in os.listdir(content_dir) if f.endswith('.md')]

    for markdown_file in markdown_files:
        # Read the markdown content along with front matter
        with open(os.path.join(content_dir, markdown_file), 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)

        # Extract layout information from front matter or use a default layout
        layout = post.get('layout', 'base.html')

        # Convert markdown to HTML
        html_content = convert_markdown_to_html(post.content)

        # Prepare the context for rendering the template
        context = {'content': html_content}

        # Determine the output file path
        output_file_path = os.path.join(output_dir, os.path.splitext(markdown_file)[0] + '.html')

        # Render the specified layout template and write to the output file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(render_template(layout, context))

if __name__ == '__main__':
    generate_static_site()
