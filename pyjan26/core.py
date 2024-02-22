import os
import shutil
import json
import glob
#import markdown2
import frontmatter  # type: ignore
from importlib import import_module
from jinja2 import Environment, FileSystemLoader, BaseLoader
from jinja2_markdown import MarkdownExtension  # type: ignore
from typing import List, Dict, Any, Union, Callable, Tuple
from pyjan26.registry import (
    CUSTOM_PAGE_REGISTRY, CUSTOM_COLLECTION_REGISTRY, 
    CUSTOM_FILTER_REGISTRY
)

#import settings
settings_module = os.environ.setdefault('PYJAN26_SETTINGS_MODULE', 'settings')
settings = import_module(settings_module) # type: ignore

# Get only variables from settings module
settings_variables = {key: value for key, value in settings.__dict__.items() if not key.startswith('__')}

def copy_static_files(static_paths: List[str], output_directory: str) -> None:
    """
    Copy static files specified in static_paths to the output_directory.
    
    Parameters:
        static_paths (list): A list of paths to static files or directories.
        output_directory (str): The directory where static files will be copied.
    """
    #TODO: use wild cards??  ex. */robots.txt ?
    for path in static_paths:
        source_path = os.path.join(os.getcwd(), path)
        destination_path = os.path.join(output_directory, path)

        if settings.DEBUG:
            print(f'STATIC FILES: source_path: {source_path}')
            print(f'STATIC FILES: destination_path: {destination_path}')
        
        if os.path.isfile(source_path):
            os.makedirs(destination_path, exist_ok=True)
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)  # Delete existing destination directory
            shutil.copytree(source_path, destination_path)

def paginate(collection: List[Any], page_size: int) -> List[List[Any]]:
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


def load_json_data(json_path: str) -> Dict[str, Any]:
    return json.load(open(json_path, 'r', encoding='utf-8')) if os.path.exists(json_path) else {}



class ContentParser:

    def load_markdown_data(self, md_json_path: str) -> Dict[str, Any]:
        json_path = f"{os.path.splitext(md_json_path)[0]}.json"
        return load_json_data(json_path)

    def parse(self, markdown_file: str) -> Tuple[frontmatter.Post, Dict[str, Any]]:
        with open(markdown_file, 'r', encoding='utf-8') as f:
            return frontmatter.load(f), self.load_markdown_data(markdown_file)

class TemplateRenderer:
    def __init__(self, templates_dir: str) -> None:
        #self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            extensions=[MarkdownExtension],
        )

        self.custom_filters: List[Callable] = []

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        template = self.env.get_template(template_name)
        return template.render(context)

    def render_string(self, content: str, context: Dict[str, Any]) -> str:
        template = self.env.from_string(content)
        return template.render(context)

    def add_filters(self, custom_function: List[Callable]) -> None:
        self.custom_filters.extend(custom_function)

    def build_custom_filters(self) -> None:
        # Build filters using custom filters functions
        # make use of function name
        for custom_filter in self.custom_filters:
            #print(custom_filter().__name__, custom_filter)
            self.env.filters[custom_filter.__name__] = custom_filter

class FileGenerator:
    def generate(self, out_dir: str, final_path: str, rendered_template: str) -> None:

        os.makedirs(out_dir, exist_ok=True)

        with open(final_path, 'w', encoding='utf-8') as f:
            f.write(rendered_template)

        if settings.DEBUG:
            print('FILE GENERATOR: makedirs', out_dir)
            print(f'FILE GENERATOR: write_to_file {final_path}')

def get_markdown_files(content_dir: str) -> List[str]:
    return glob.glob(os.path.join(content_dir, "**/*.md"), recursive=True)

def render_string(content: str, context: Dict[str, Any]) -> str:
    template_renderer = TemplateRenderer(settings.TEMPLATE_DIR)
    results = template_renderer.render_string(content, context)
    return results

def render_template(template_name: str, context: Dict[str, Any]) -> str:
    template_renderer = TemplateRenderer(settings.TEMPLATE_DIR)
    results = template_renderer.render(template_name, context)
    return results

def generate_file(out_dir: str, final_out: str, rendered_template: str) -> None:
    file_generator = FileGenerator()
    return file_generator.generate(out_dir, final_out, rendered_template)

def get_output_directory(collection_name: str, out_dir: str | None, page_num: int | None, items: Dict[str, Any]) -> str:

    if out_dir:
        out_dir = f'{settings.OUTPUT_DIR}/{out_dir}'
        #template_rendererender = TemplateRenderer(settings.TEMPLATE_DIR)
        #out_dir = template_renderer.render_string(out_dir, items)
        out_dir = render_string(out_dir, items)
    elif page_num:
        out_dir = f'{settings.OUTPUT_DIR}/{collection_name}/{page_num}'
    else:
        base_name = os.path.splitext(items['base_name'])[0]
        if base_name == 'index' and collection_name == settings.CONTENT_DIR:
            out_dir = settings.OUTPUT_DIR
        elif base_name == 'index':
            out_dir = f'{settings.OUTPUT_DIR}/{collection_name}'
        elif collection_name == settings.CONTENT_DIR:
            out_dir = f'{settings.OUTPUT_DIR}/{base_name}'
        else:
            out_dir = f'{settings.OUTPUT_DIR}/{collection_name}/{base_name}'
    return out_dir

def render_page(page_data: Dict[str, Any], page_num: Union[int, None] = None) -> None:
    #template_renderer = TemplateRenderer(settings.TEMPLATE_DIR)    

    collections = page_data.get('collections', {})
    items = page_data.get('items', {})
    settings2 = page_data.get('settings', {})
    collection_name = page_data.get('collection_name', '')
    pagination = page_data.get('pagination', {})

    #should we mov under pagination dict?
    page_items = page_data.get('page_items', {})
    alias = page_data.get('alias')

    #custom output directory?
    out_dir = page_data.get('out_dir')

    if settings.DEBUG:
        if out_dir: print(f'RENDER_PAGE: custom out_dir {out_dir}')


    context = {
        **items,
        'collections': collections, 
        'settings': settings2,
        'pagination': pagination,
        **({alias : page_items} if page_items else {})
    }

    # Render Markdown HTML content
    html_content = render_string(items['content'], context)
    
    out_dir = get_output_directory(collection_name, out_dir, page_num, items)


    final_out = f'{out_dir}/index.html'


    rendered_template = render_template(
        page_data['items']['layout'], 
        {'content': html_content, 
            'collections': collections, 
            'settings': settings2, 
            'pagination': pagination
            }
    )
    #import pprint
    #pprint.pprint({'content': html_content, **context})
    generate_file(out_dir, final_out, rendered_template)


class Jan26Gen:
    def __init__(self):
        self.template_dir = os.getenv('TEMPLATE_DIR', settings.TEMPLATE_DIR)
        self.content_dir = os.getenv('CONTENT_DIR', settings.CONTENT_DIR)
        self.output_dir = os.getenv('OUTPUT_DIR', settings.OUTPUT_DIR)
        self.default_layout = os.getenv('DEFAULT_LAYOUT', settings.DEFAULT_LAYOUT)

        self.content_parser = ContentParser()
        self.template_renderer = TemplateRenderer(self.template_dir)
        self.custom_collections: List[Callable] = []

        if CUSTOM_FILTER_REGISTRY:
            self.template_renderer.add_filters(CUSTOM_FILTER_REGISTRY)

        if CUSTOM_COLLECTION_REGISTRY:
            self.custom_collections.extend(CUSTOM_COLLECTION_REGISTRY)

    #def add_filters(self, custom_filters: List[Callable]) -> None:
    #    self.template_renderer.add_filters(custom_filters)

    #def add_collections(self, custom_function: List[Callable]) -> None:
    #    self.custom_collections.extend(custom_function)

    def build_custom_collections(self, collections: Dict[str, Any]) -> Dict[str, Any]:
        # Build collections using custom collection functions
        for function in self.custom_collections:
            custom_collections = function(collections)
            for name, items in custom_collections.items():
                if isinstance(items, list):
                    collections.setdefault(name, []).extend(items)
                else:
                    collections.setdefault(name, items)

        return collections

    def build_collections(self) -> Dict[str, Any]:
        markdown_files = get_markdown_files(self.content_dir)
        collections: Dict[str, Dict] = { 'collections': {} }

        for markdown_file in markdown_files:
            frontmatter_data, markdown_data_dict = self.content_parser.parse(markdown_file)  
            collection_name = os.path.basename(os.path.dirname(markdown_file))

            context = {
                **markdown_data_dict, 
                **frontmatter_data.to_dict(),
                'layout': frontmatter_data.get('layout', self.default_layout),
                'base_name': os.path.basename(markdown_file)
            }

            if collection_name not in collections['collections']:
                collections['collections'][collection_name] = []

            collections['collections'][collection_name].append(context)


        collections.update({'settings' : settings_variables})

        collections['collections'] = self.build_custom_collections(collections['collections'])

        return collections

    def render_collections(self, objs: Dict[str, Any]) -> None:
        collections = objs.get('collections', {})
        settings2 = objs.get('settings', {})
        skip_next = None

        for collection_name, items in collections.items():
            for item in items:
                if isinstance(item, dict) and item.get('base_name'):
                    out_dir = item.get('out_dir')
                    for pre_condition, custom_page_fn in CUSTOM_PAGE_REGISTRY.items():
                        if item.get(pre_condition):
                            result = custom_page_fn(item, collection_name, collections, settings, out_dir=out_dir)
                            skip_next = result.get('skip_next')
                            

                    #print('still goes here??')
                    # skip other condition w/in the same page
                    if skip_next in (None, False):
                        if item.get('paginated'):
                            self.render_paginated_collection(item, collection_name, collections, settings, out_dir=out_dir)
                        else:
                            page_data = {
                                'collection_name': collection_name, 
                                'collections': collections,  
                                'settings': settings2, 
                                'items': item,
                                'out_dir': out_dir
                            }
                            render_page(page_data)
    
    def remove_index(self, page_items, items):
        # should not include index file in the paginated items
        return [p_item for p_item in page_items if p_item.get('base_name') != items['base_name'] ]

    def generate_url(self, out_dir, items, page_items, collection_name):
        for item in page_items:
            if out_dir:
                out_dir =  render_string(out_dir, item)
                item['url'] = f'/{collection_name}/{out_dir}'
            else:
                base_name = os.path.splitext(item['base_name'])[0]
                item['url'] = f'/{collection_name}/{base_name}'

            if settings.DEBUG:
                print(f'GENERATE_URL: item {item}')
                print(f'GENERATE_URL: out_dir {out_dir}')
                print(f'GENERATE_URL: item["url"] {item["url"]}')
        return page_items, out_dir

    def get_pagination_metadata(self, out_dir, page_num, collection_name, total_pages, page_numbers, page_items):
        if out_dir:
            out_dir =  render_string(out_dir, page_items[0])
            #out_dir = self.render_output_directory(out_dir, page_items[0])
            out_dir = f'/{collection_name}/{out_dir}'
            page_number_links = [{ 'page_number': page_number, 'url': f'{out_dir}/{page_number}' } for page_number in page_numbers]
        else:
            page_number_links = [{ 'page_number': page_number, 'url': f'/{collection_name}/{page_number}' } for page_number in page_numbers]

        prev_page_num = page_num - 1 if page_num > 1 else None
        next_page_num = page_num + 1 if page_num < total_pages else None
        prev_page_url = f"/{out_dir}/{prev_page_num}" if out_dir and prev_page_num else f"/{collection_name}/{prev_page_num}" if prev_page_num else None
        next_page_url = f"/{out_dir}/{next_page_num}" if out_dir and next_page_num else f"/{collection_name}/{next_page_num}" if next_page_num else None

        pagination = {
            'page_number': page_num,
            'page_numbers': page_number_links,
            'total_pages': total_pages,
            'prev_page': prev_page_url,
            'next_page': next_page_url
        }
        return pagination

    def render_paginated_collection(self, items, collection_name, collections, settings2, out_dir=None):
        paginated = items.get('paginated', {})

        paginated_items = self.remove_index(collections.get(paginated.get('items'), []), items)
        page_size = paginated.get('size', settings.PAGE_SIZE)
        alias = paginated.get('alias', f'paginated{collection_name.title()}')
        paginated_list = paginate(paginated_items, page_size)
        total_pages = len(paginated_list)
        page_numbers= list(range(1, total_pages + 1))

        for page_num, page_items in enumerate(paginated_list, start=1):
            #print(f"Page {page_num}: {page_items}")

            # Generate URLs for each page_item
            page_items_w_urls, out_dir = self.generate_url(out_dir, items, page_items, collection_name)

            pagination_metadata = self.get_pagination_metadata(out_dir, page_num, collection_name, total_pages, page_numbers, page_items)


            page_data = {
                'collection_name': collection_name,
                'collections': collections,
                'settings': settings2,
                'items': items,
                'alias': alias,
                'page_items': page_items_w_urls, 
                'pagination': pagination_metadata,
                'out_dir': out_dir
            }

            if settings.DEBUG:
                print(f'RENDER_PAGINATED: page_data: {page_data}')

            render_page(page_data, page_num)

    def generate_site(self):
        self.template_renderer.build_custom_filters()
        collections = self.build_collections()
        self.render_collections(collections)
        
        copy_static_files(settings.STATIC_PATHS, self.output_dir)

