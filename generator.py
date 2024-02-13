import os
import json
import glob
#import markdown2
import frontmatter
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension

import settings

# Get only variables from settings module
settings_variables = {key: value for key, value in settings.__dict__.items() if not key.startswith('__')}


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
    def generate(self, out_dir, final_path, rendered_template):

        os.makedirs(out_dir, exist_ok=True)
        print('makedirs', out_dir)

        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)

        print(f'write_to_file {final_path}')

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
        collections = { 'collections': {} }

        for markdown_file in markdown_files:
            frontmatter_data, markdown_data_dict = self.content_parser.parse(markdown_file)  
            collection_name = os.path.basename(os.path.dirname(markdown_file))

            context = {
                **markdown_data_dict, 
                **frontmatter_data.to_dict(),
                'layout': frontmatter_data.get('layout', self.default_layout),
                'file_name': os.path.basename(markdown_file)
            }

            #permalink = frontmatter_data.get('out_path')
            #if permalink:
            #    context.update({'out_path': self.template_renderer.render_string(permalink, context_w_global_dict)})
            #else:
            #    context.update({'out_path': f'{os.path.splitext(markdown_file.lstrip(self.content_dir))[0].rstrip("/index")}/index.html' })


            if collection_name not in collections['collections']:
                collections['collections'][collection_name] = []

            collections['collections'][collection_name].append(context)


        collections.update({'settings' : settings_variables})

        collections['collections'] = self.build_custom_collections(collections['collections'])

        return collections

    def render_collections(self, objs):
        collections = objs.get('collections', {})
        settings = objs.get('settings', {})

        for collection_name, items in collections.items():
            for item in items:
                if isinstance(item, dict) and item.get('file_name'):
                    if item.get('paginated'):
                        self.render_paginated_collection(item, collection_name, collections, settings)
                    else:
                        page_data = {
                            'collection_name': collection_name, 
                            'collections': collections,  
                            'settings': settings, 
                            'items': item 
                        }
                        self.render_page(page_data)
    
    def remove_index(self, page_items, items):
        # should not include index file in the paginated items
        return [p_item for p_item in page_items if p_item['file_name'] != items['file_name'] ]

    def generate_url(self, page_items, collection_name):
        for item in page_items:
            # Replace 'generate_url' with your logic to generate the URL
            file_name = os.path.splitext(item['file_name'])[0]
            item['url'] = f'/{collection_name}/{file_name}'
        return page_items

    def render_paginated_collection(self, items, collection_name, collections, settings):
        paginated = items.get('paginated', {})

        paginated_items = self.remove_index(collections.get(paginated.get('items'), []), items)
        page_size = paginated.get('size', settings.get('PAGE_SIZE') )
        alias = paginated.get('alias', f'paginated{collection_name.title()}')
        paginated_list = paginate(paginated_items, page_size)
        total_pages = len(paginated_list)

        for page_num, page_items in enumerate(paginated_list, start=1):
            #print(f"Page {page_num}: {page_items}")

            # Generate URLs for each page_item
            page_items = self.generate_url(page_items, collection_name)

            prev_page_num = page_num - 1 if page_num > 1 else None
            next_page_num = page_num + 1 if page_num < total_pages else None

            # Construct URLs for prev_page and next_page
            prev_page_url = f"/{collection_name}/{prev_page_num}" if prev_page_num else None
            next_page_url = f"/{collection_name}/{next_page_num}" if next_page_num else None

            pagination = {
                'page_num': page_num,
                'total_pages': total_pages,
                'prev_page': prev_page_url,
                'next_page': next_page_url
            }

            page_data = {
                'collection_name': collection_name,
                'collections': collections,
                'settings': settings,
                'items': items,
                'alias': alias,
                'page_items': page_items, 
                'pagination': pagination
            }
            self.render_page(page_data, page_num)


    def render_page(self, page_data, page_num=None):
        collections = page_data.get('collections', {})
        items = page_data.get('items', {})
        settings = page_data.get('settings', {})
        collection_name = page_data.get('collection_name', '')
        pagination = page_data.get('pagination', {})

        #should we mov under pagination dict?
        page_items = page_data.get('page_items', {})
        alias = page_data.get('alias')

        context = {
            **items,
            'collections': collections, 
            'settings': settings,
            'pagination': pagination,
            **({alias : page_items} if page_items else {})
        }
        #import pprint
        #pprint.pprint(context)


        # Extract file name from item
        file_name = os.path.splitext(items['file_name'])[0]

        # Render Markdown HTML content
        html_content = self.template_renderer.render_string(items['content'], context)

        if page_num:
            out_dir = f'{self.output_dir}/{collection_name}/{page_num}'
        elif file_name == 'index' and collection_name == self.content_dir:
            out_dir = self.output_dir
        elif file_name == 'index':
            out_dir = f'{self.output_dir}/{collection_name}'
        elif collection_name == self.content_dir:
            out_dir = f'{self.output_dir}/{file_name}'
        else:
            out_dir = f'{self.output_dir}/{collection_name}/{file_name}'

        final_out = f'{out_dir}/index.html'


        rendered_template = self.template_renderer.render(
            page_data['items']['layout'], 
            {'content': html_content, 'collections': collections, 'settings': settings}
        )
        #import pprint
        #pprint.pprint({'content': html_content, **context})
        self.file_generator.generate(out_dir, final_out, rendered_template)

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


