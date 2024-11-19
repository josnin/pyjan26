import pprint
import os
import pkg_resources
import shutil
import json
import glob
import markdown
import frontmatter  # type: ignore
from importlib import import_module
from jinja2 import Environment, FileSystemLoader, BaseLoader
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
        self.env = Environment(loader=FileSystemLoader(templates_dir))

        self.custom_filters: List[Callable] = []

        if CUSTOM_FILTER_REGISTRY:
            self.add_filters(CUSTOM_FILTER_REGISTRY)
            self.build_custom_filters()

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
            print(f'FILE GENERATOR: makedirs {out_dir}')
            print(f'FILE GENERATOR: write_to_file {final_path}')

def get_markdown_files(include_files=None) -> List[str]:
    if include_files:
        return glob.glob(include_files)
    return glob.glob(os.path.join(settings.CONTENT_DIR, "**/*.md"), recursive=True)

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

def get_output_directory(collection_name: str, permalink: str | None, page_num: int | None, items: Dict[str, Any]) -> str:
    output_dir = settings.OUTPUT_DIR

    #TODO: added condition first if condition should not goes for item w pagination 
    if permalink and not page_num:
        if collection_name != settings.CONTENT_DIR: # make sure its folder collections
            output_dir = os.path.join(output_dir, collection_name, permalink)
        else:
            output_dir = os.path.join(output_dir, permalink)
        output_dir = render_string(output_dir, items)
    elif permalink and page_num:
        output_dir = os.path.join(output_dir, collection_name, permalink, str(page_num))
    elif page_num:
        output_dir = os.path.join(output_dir, collection_name, str(page_num))
    else:
        base_name = os.path.splitext(items['base_name'])[0]
        if base_name == 'index' and collection_name == settings.CONTENT_DIR:
            output_dir = settings.OUTPUT_DIR
        elif base_name == 'index':
            output_dir = os.path.join(output_dir, collection_name)
        elif collection_name == settings.CONTENT_DIR:
            output_dir = os.path.join(output_dir, base_name)
        else:
            output_dir = os.path.join(output_dir, collection_name, base_name)
    
    return output_dir

def render_page(page_data: Dict[str, Any], page_num: Union[int, None] = None) -> None:
    #template_renderer = TemplateRenderer(settings.TEMPLATE_DIR)    

    collections = page_data.get('collections', {})
    items = page_data.get('items', {})
    settings2 = page_data.get('settings', {})
    collection_name = page_data.get('collection_name', '')
    pagination = page_data.get('pagination', {})
    page_items = page_data.get('page_items', {})
    alias = page_data.get('alias')

    if items:
        permalink = items.get('permalink')



    context = {
        **items,
        'collections': collections, 
        'settings': settings2,
        'pagination': pagination,
    }
    if page_items:
        context[alias] = page_items

    # Render Markdown HTML content
    html_content = render_string(
            markdown.markdown(items['content']), 
            context
        )
    
    out_dir2 = get_output_directory(collection_name, permalink, page_num, items)

    if is_filepath(out_dir2):
        # do this if the dir path is provided
        # ex. post/post.html
        final_out = out_dir2
        out_dir2 = '/'.join(out_dir2.split('/')[:-1])
    else:
        final_out = os.path.join(out_dir2, 'index.html')
    #final_out = f'{out_dir2}/index.html'


    rendered_template = render_template(
        page_data['items']['layout'], 
        {'content': html_content, 
            'collections': collections, 
            'settings': settings2, 
            'pagination': pagination
            }
    )

    print(f'RENDER_PAGE: output_dir {out_dir2}  output file {final_out}')
    generate_file(out_dir2, final_out, rendered_template)

def is_filepath(out_dir: str):
    _, ext = os.path.splitext(out_dir)
    return bool(ext)


class PyJan26:
    def __init__(self, markdown_files):
        self.template_dir = os.getenv('TEMPLATE_DIR', settings.TEMPLATE_DIR)
        self.content_dir = os.getenv('CONTENT_DIR', settings.CONTENT_DIR)
        self.output_dir = os.getenv('OUTPUT_DIR', settings.OUTPUT_DIR)
        self.default_layout = os.getenv('DEFAULT_LAYOUT', settings.DEFAULT_LAYOUT)

        self.content_parser = ContentParser()
        self.custom_collections: List[Callable] = []

        self.markdown_files = markdown_files

        if CUSTOM_COLLECTION_REGISTRY:
            self.custom_collections.extend(CUSTOM_COLLECTION_REGISTRY)

    #def add_filters(self, custom_filters: List[Callable]) -> None:
    #    self.template_renderer.add_filters(custom_filters)

    #def add_collections(self, custom_function: List[Callable]) -> None:
    #    self.custom_collections.extend(custom_function)

    def build_custom_collections(self, collections: Dict[str, Any]) -> Dict[str, Any]:
        # Build collections using custom collection functions
        custom_names: List[str] = []
        for function in self.custom_collections:
            custom_collections = function(collections)
            for name, items in custom_collections.items():
                custom_names.append(name)
                if isinstance(items, list):
                    collections.setdefault(name, []).extend(items)
                else:
                    collections.setdefault(name, items) #if a non list
        return collections, custom_names

    def build_collections(self) -> Dict[str, Any]:
        #markdown_files = get_markdown_files(self.content_dir)
        collections: Dict[str, Dict] = { 'collections': {} }

        for markdown_file in self.markdown_files:
            frontmatter_data, markdown_data_dict = self.content_parser.parse(markdown_file)  
            collection_name = os.path.basename(os.path.dirname(markdown_file))

            context = {
                **markdown_data_dict, 
                **frontmatter_data.to_dict(),
                'layout': frontmatter_data.get('layout', self.default_layout),
                'base_name': os.path.basename(markdown_file),
                'name': os.path.splitext(os.path.basename(markdown_file))[0],
            }

            if collection_name not in collections['collections']:
                collections['collections'][collection_name] = []

            collections['collections'][collection_name].append(context)


        collections.update({'settings' : settings_variables})

        collections['collections'], collections['custom_collection_names']  = self.build_custom_collections(collections['collections'])

        print(f'BUILD COLLECTIONS:')
        if settings.DEBUG:
            pprint.pprint(collections)

        return collections

    def render_collections(self, objs: Dict[str, Any]) -> None:
        collections = objs.get('collections', {})
        custom_collection_names = objs.get('custom_collection_names', {})
        settings2 = objs.get('settings', {})
        skip_next = None

        for collection_name, items in collections.items():
            for item in items:
                if isinstance(item, dict) and item.get('base_name'):
                    for pre_condition, custom_page_fn in CUSTOM_PAGE_REGISTRY.items():
                        if item.get(pre_condition):
                            result = custom_page_fn(item, collection_name, collections, settings2)
                            skip_next = result.get('skip_next')
                            

                    #print('still goes here??')
                    # skip other condition w/in the same page
                    if skip_next in (None, False):
                        if item.get('paginated'):
                            self.render_paginated_collection(item, collection_name, collections, settings2)
                        else:
                            page_data = {
                                'collection_name': collection_name, 
                                'collections': collections,  
                                'settings': settings2, 
                                'items': item,
                            }
                            if not collection_name in custom_collection_names:
                                render_page(page_data)
    

    def get_pagination_metadata(self, permalink, page_num, items, collection_name, total_pages, page_numbers, page_items):
        if permalink: 
            # if paginated, page size is 1 , and each url's has different naming then it wont make sense to have a pagination metadata
            # it will generate but will not make sense & be useful for diff naming
            permalink =  render_string(permalink, { **page_items[0], **items } )
            permalink = f'{collection_name}/{permalink}'
            page_number_links = [{ 'page_number': page_number, 'url': f'/{permalink}/{page_number}' } for page_number in page_numbers]
        else:
            page_number_links = [{ 'page_number': page_number, 'url': f'/{collection_name}/{page_number}' } for page_number in page_numbers]

        prev_page_num = page_num - 1 if page_num > 1 else None
        next_page_num = page_num + 1 if page_num < total_pages else None
        prev_page_url = f"/{permalink}/{prev_page_num}" if permalink and prev_page_num else f"/{collection_name}/{prev_page_num}" if prev_page_num else None
        next_page_url = f"/{permalink}/{next_page_num}" if permalink and next_page_num else f"/{collection_name}/{next_page_num}" if next_page_num else None

        pagination = {
            'page_number': page_num,
            'page_numbers': page_number_links,
            'total_pages': total_pages,
            'prev_page': prev_page_url,
            'next_page': next_page_url
        }
        return pagination

    def render_paginated_collection(self, items, collection_name, collections, settings2):
        paginated = items.get('paginated', {})

        paginated_items = collections.get(paginated.get('items'), [])
        page_size = paginated.get('size', settings.PAGE_SIZE)
        alias = paginated.get('alias', paginated.get('items'))
        paginated_list = paginate(paginated_items, page_size)
        total_pages = len(paginated_list)
        page_numbers = list(range(1, total_pages + 1))
        permalink = items.get('permalink')


        for page_num, page_items in enumerate(paginated_list, start=1):
            #print(f"Page {page_num}: {page_items}")

            # Generate URLs for each page_item
            # better to define it directly in template?
            #page_items_w_urls, out_dir2 = self.generate_url(out_dir, page_num, page_items, collection_name)

            pagination_metadata = self.get_pagination_metadata(permalink, page_num, items, collection_name, total_pages, page_numbers, page_items)


            page_data = {
                'collection_name': collection_name,
                'collections': collections,
                'settings': settings2,
                'items': items,
                'alias': alias,
                'page_items': page_items, 
                'pagination': pagination_metadata,
                'out_dir': out_dir2
            }

            print(f'RENDER_PAGINATED: collection_name {collection_name} w page_num {page_num}')
            if settings.DEBUG:
                pprint.pprint(page_data)

            render_page(page_data, page_num)


            # to provide default index.html, for ex. posts/index.html
            # its a equivalent of posts/1/index.html 
            if page_num == 1:
                print(f'RENDER_PAGINATED: collection_name {collection_name} w index.html equivalent of page_num 1')
                render_page(page_data, None)


    def generate_site(self):
        collections = self.build_collections()

        self.render_collections(collections)
        
        copy_static_files(settings.STATIC_PATHS, self.output_dir)

