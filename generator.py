import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension

import settings

# Get only variables from settings module
settings_variables = {key.lower() : value for key, value in settings.__dict__.items() if not key.startswith('__')}


def paginate(collection, page_size):
    """
    Convert a collection list into a paginated list.
    
    Parameters:
        collection (list): The original collection list.
        page_size (int): The number of items per page.
        
    Returns:
        list: A list of pages, where each page is a sublist of the original collection.
    """
    paginated_list = []
    for i in range(0, len(collection), page_size):
        paginated_list.append(collection[i:i + page_size])
    return paginated_list

## Example usage:
collection_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
page_size = 3
paginated_list = paginate(collection_list, page_size)
for page_number, page_items in enumerate(paginated_list, start=1):
    print(f"Page {page_number}: {page_items}")



def load_json_data(json_path):
    return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}

def get_custom_collections_fn():
    res = None
    try:
        import custom_collections

        # Get all function names from the module
        function_names = [name for name in dir(custom_collections) if callable(getattr(custom_collections, name))]

        # Get the function objects using getattr() and pass them to add_collections
        res = [getattr(custom_collections, name) for name in function_names]

    except ImportError:
        print("custom_collections.py file not found. No custom collections will be added.")

    return res

def get_custom_filters_fn():
    res = None
    try:
        import custom_filters

        # Get all function names from the module
        function_names = [name for name in dir(custom_filters) if callable(getattr(custom_filters, name))]

        # Get the function objects using getattr() and pass them to add_filters
        res = [getattr(custom_filters, name) for name in function_names]

    except ImportError:
        print("custom_filters.py file not found. No custom filters will be added.")
    
    return res

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

        self.custom_filters = []

    def render(self, template_name, context):
        template = self.env.get_template(template_name)
        return template.render(context)

    def render_string(self, content, context):
        template = self.env.from_string(content)
        return template.render(context)

    def add_filters(self, custom_function):
        self.custom_filters.extend(custom_function)

    def build_custom_filters(self):
        # Build filters using custom filters functions
        # make use of function name
        for custom_filter in self.custom_filters:
            #print(custom_filter().__name__, custom_filter)
            self.env.filters[custom_filter.__name__] = custom_filter

class FileGenerator:
    def generate(self, out_dir_name, final_out_path, write_to_file):

        os.makedirs(out_dir_name, exist_ok=True)
        print('makedirs', out_dir_name)

        with open(final_out_path, 'w', encoding='utf-8') as f:
            f.write(write_to_file)

        print(f'write_to_file {final_out_path}')

    def get_markdown_files(self, content_dir):
        return glob.glob(os.path.join(content_dir, "**/*.md"), recursive=True)


class Jan26Gen:
    def __init__(self):
        self.template_dir = os.getenv('TEMPLATE_DIR', settings.TEMPLATE_DIR)
        self.content_dir = os.getenv('CONTENT_DIR', settings.CONTENT_DIR)
        self.output_dir = os.getenv('OUTPUT_DIR', settings.OUTPUT_DIR)
        self.default_layout = os.getenv('DEFAULT_LAYOUT', settings.DEFAULT_LAYOUT)

        self.content_parser = ContentParser()
        self.template_renderer = TemplateRenderer(self.template_dir)
        self.file_generator = FileGenerator()
        self.custom_collections = []

    def add_filters(self, custom_filters):
        self.template_renderer.add_filters(custom_filters)

    def add_collections(self, custom_function):
        self.custom_collections.extend(custom_function)

    def build_custom_collections(self, collections):
        # Build collections using custom collection functions
        for function in self.custom_collections:
            custom_collections = function(collections)
            for name, items in custom_collections.items():
                if isinstance(items, list):
                    collections.setdefault(name, []).extend(items)
                else:
                    collections.setdefault(name, items)

        return collections

    def build_collections(self):
        markdown_files = self.file_generator.get_markdown_files(self.content_dir)
        collections = {}

        for markdown_file in markdown_files:
            frontmatter_data, markdown_data_dict = self.content_parser.parse(markdown_file)  
            collection_name = os.path.basename(os.path.dirname(markdown_file))

            # predefined collections starts here

            context = {**markdown_data_dict, **frontmatter_data.to_dict()}
            context_w_global_dict = { **context, **settings_variables }

            layout = frontmatter_data.get('layout', self.default_layout)
            context.update({'layout': layout})

            #permalink = frontmatter_data.get('out_path')
            #if permalink:
            #    context.update({'out_path': self.template_renderer.render_string(permalink, context_w_global_dict)})
            #else:
            #    context.update({'out_path': f'{os.path.splitext(markdown_file.lstrip(self.content_dir))[0].rstrip("/index")}/index.html' })

            context.update({'file_name': os.path.basename(markdown_file)})

            if collection_name not in collections:
                collections[collection_name] = []

            collections[collection_name].append(context)


        collections.update(settings_variables)

        collections = self.build_custom_collections(collections)

        return collections

    def render_collections(self, collections):

        for collection_name, items in collections.items():
            for item in items:
                if isinstance(item, dict) and item.get('file_name'):
                    if item.get('page_size') and item.get('paginated_items'):
                        #items = collections.get(item['pagination_items'])
                        self.render_paginated_collection(item, collection_name, collections)
                    #elif item.get('page_size'):
                    #    self.render_paginated_collection(items, collection_name, collections)
                    else:
                        page_data = {'collection_name': collection_name, 'items': item }
                        self.render_page(page_data, collection_name, collections, 1)

    def render_paginated_collection(self, items, collection_name, collections):
        # Example usage:
        page_size = items.get('page_size')
        items = collections[items.get('paginated_items')]
        paginated_list = paginate(items, page_size)
        import pdb; pdb.set_trace()
        print(f'paginated_list {paginated_list}')
        for page_num, page_items in enumerate(paginated_list, start=1):
            print(f"Page {page_num}: {page_items}")
            page_data = {'collection_name': collection_name, 'items': items }
            self.render_page(page_data, collection_name, collections, page_num)

    def render_page(self, page_data, collection_name, collections, page_num=None):
        item_w_collections = { **page_data['items'], **collections}
        file_name = os.path.splitext(page_data['items']['file_name'])[0]
        html_content = self.template_renderer.render_string(page_data['items']['content'], item_w_collections)

        if file_name == 'index': 
            final_out_path = f"{self.output_dir}/{collection_name}/index.html"
            out_dir_name = f'{self.output_dir}/{collection_name}'
        elif page_num:
            final_out_path = f"{self.output_dir}/{collection_name}/{page_num}/index.html"
            out_dir_name = f'{self.output_dir}/{collection_name}/{page_num}'
        else:
            final_out_path = f"{self.output_dir}/{collection_name}/{file_name}/index.html"
            out_dir_name = f'{self.output_dir}/{collection_name}'


        write_to_file = self.template_renderer.render(page_data['items']['layout'], {'content': html_content, **collections })
        self.file_generator.generate(out_dir_name, final_out_path, write_to_file)

    def generate_site(self):
        self.template_renderer.build_custom_filters()
        collections = self.build_collections()
        self.render_collections(collections)


if __name__ == '__main__':

    custom_collections_fn = get_custom_collections_fn()
    custom_filters_fn = get_custom_filters_fn()


    gen = Jan26Gen()
    if custom_filters_fn: gen.add_filters(custom_filters_fn)
    if custom_collections_fn: gen.add_collections(custom_collections_fn)
    print(gen.generate_site())


