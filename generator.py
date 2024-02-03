import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension
from settings import *


class Jan26Gen:
    def __init__(self):
        self.template_dir = os.getenv('TEMPLATE_DIR', TEMPLATE_DIR)
        self.content_dir = os.getenv('CONTENT_DIR', CONTENT_DIR)
        self.global_data_dir = os.getenv('GLOBAL_DATA_DIR', GLOBAL_DATA_DIR)
        self.output_dir = os.getenv('OUTPUT_DIR', OUTPUT_DIR)
        self.default_layout = os.getenv('DEFAULT_LAYOUT', DEFAULT_LAYOUT)

        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            extensions=[MarkdownExtension],
        )

    def process_markdown(self):
        markdown_files = glob.glob(os.path.join(self.content_dir, "**/*.md"), recursive=True)
        global_data_dict = self.load_global_data()

        for markdown_file in markdown_files:
            frontmatter_data, markdown_data_dict = self.load_data(markdown_file)
            context = {**global_data_dict, **markdown_data_dict, **frontmatter_data.to_dict()}

            layout = frontmatter_data.get('layout', self.default_layout)
            permalink = frontmatter_data.get('permalink')

            html_content = self.render_string(frontmatter_data.content, context)

            out_path = os.path.join(self.output_dir, self.render_string(permalink, context)) if permalink else markdown_file.replace(self.content_dir, self.output_dir)

            out_dir_name = os.path.splitext(out_path)[0]
            os.makedirs(out_dir_name, exist_ok=True)
            print('makedirs', out_dir_name)

            final_out_path = self.get_final_out_path(out_path)
            print('write here', final_out_path)

            self.write_to_file(final_out_path, layout, html_content, context)

    def load_global_data(self):
        return {os.path.splitext(f)[0]: self.load_json_data(os.path.join(self.global_data_dir, f)) for f in os.listdir(self.global_data_dir) if f.endswith('.json')}

    def load_data(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return frontmatter.load(f), self.load_markdown_data(markdown_file)

    def load_markdown_data(self, md_json_path):
        json_path = f"{os.path.splitext(md_json_path)[0]}.json"
        return self.load_json_data(json_path)

    def load_json_data(self, json_path):
        return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}

    def render_template(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)

    def render_string(self, md_content, context):
        template = self.env.from_string(md_content)
        return template.render(context)

    def get_final_out_path(self, out_path):
        return f"{os.path.splitext(out_path)[0]}.html" if out_path.endswith('index.md') else os.path.join(os.path.splitext(out_path)[0], "index.html")

    def write_to_file(self, final_out_path, layout, html_content, context):
        with open(final_out_path, 'w', encoding='utf-8') as f:
            context.pop('content')
            f.write(self.render_template(layout, {'content': html_content, **context }))

    def generate_static_site(self):
        self.process_markdown()


if __name__ == '__main__':
    ssg = Jan26Gen()
    ssg.generate_static_site()
