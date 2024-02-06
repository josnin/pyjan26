import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension
from settings import *

def load_json_data(json_path):
    return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}

class ContentParser:

    def load_markdown_data(self, md_json_path):
        json_path = f"{os.path.splitext(md_json_path)[0]}.json"
        return load_json_data(json_path)

    def parse(self, markdown_file):
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return frontmatter.load(f), self.load_markdown_data(markdown_file)

class TemplateRenderer:
    def __init__(self, templates_dir):
        #self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            extensions=[MarkdownExtension],
        )

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)

    def render_string(self, content, context):
        template = self.env.from_string(content)
        return template.render(context)

class FileGenerator:
    def generate(self, out_dir_name, final_out_path, write_to_file):
        os.makedirs(out_dir_name, exist_ok=True)
        print('makedirs', out_dir_name)

        with open(final_out_path, 'w', encoding='utf-8') as f:
            f.write(write_to_file)

        print(f'write_to_file {final_out_path}')


class Jan26Gen:
    def __init__(self):
        self.template_dir = os.getenv('TEMPLATE_DIR', TEMPLATE_DIR)
        self.content_dir = os.getenv('CONTENT_DIR', CONTENT_DIR)
        self.global_data_dir = os.getenv('GLOBAL_DATA_DIR', GLOBAL_DATA_DIR)
        self.output_dir = os.getenv('OUTPUT_DIR', OUTPUT_DIR)
        self.default_layout = os.getenv('DEFAULT_LAYOUT', DEFAULT_LAYOUT)

        self.content_parser = ContentParser()
        self.template_renderer = TemplateRenderer(self.template_dir)
        self.file_generator = FileGenerator()

        self._collections = {}

    def get_markdown_files(self):
        return glob.glob(os.path.join(self.content_dir, "**/*.md"), recursive=True)

    def load_global_data(self):
        return {os.path.splitext(f)[0]: self.load_json_data(os.path.join(self.global_data_dir, f)) for f in os.listdir(self.global_data_dir) if f.endswith('.json')}

    def load_json_data(self, json_path):
        return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}

    def get_final_out_path(self, out_path):
        return f"{os.path.splitext(out_path)[0]}.html" if out_path.endswith('index.md') else os.path.join(os.path.splitext(out_path)[0], "index.html")

    def get_collections(self):
        return self._collections

    def build_collections(self):
        markdown_files = self.get_markdown_files()
        global_data_dict = self.load_global_data()

        for markdown_file in markdown_files:
            frontmatter_data, markdown_data_dict = self.content_parser.parse(markdown_file)  
            collection_name = os.path.basename(os.path.dirname(markdown_file))

            context = {**markdown_data_dict, **frontmatter_data.to_dict()}
            context_w_global_dict = { **context, **global_data_dict }

            layout = frontmatter_data.get('layout', self.default_layout)
            context.update({'layout': layout})

            permalink = frontmatter_data.get('permalink')
            if permalink:
                context.update({'permalink': self.template_renderer.render_string(permalink, context_w_global_dict)})

            html_content = self.template_renderer.render_string(frontmatter_data.content, context_w_global_dict)
            context.update({'html_content': html_content})

            out_path = os.path.join(self.output_dir, self.template_renderer.render_string(permalink, context_w_global_dict)) if permalink else markdown_file.replace(self.content_dir, self.output_dir)
            context.update({'out_path': out_path})

            out_dir_name = os.path.splitext(out_path)[0]
            context.update({'out_dir_name': out_dir_name})

            final_out_path = self.get_final_out_path(out_path)
            context.update({'final_out_path': final_out_path})

            write_to_file = self.template_renderer.render(layout, {'content': html_content, **global_data_dict })
            context.update({'write_to_file': write_to_file})

            if collection_name not in self._collections:
                self._collections[collection_name] = []

            self._collections[collection_name].append(context)
        
        self._collections.update(global_data_dict)

        #print(self.collections)

    def render_collections(self):
        self.build_collections()

        for collection_name, items in self.get_collections().items():
            for item in items:
                if 'out_dir_name' in item:
                    self.file_generator.generate(item['out_dir_name'], 
                                                 item['final_out_path'], item['write_to_file'])

    def generate_static_site(self):
        self.render_collections()


if __name__ == '__main__':
    s = Jan26Gen()
    print(s.generate_static_site())
