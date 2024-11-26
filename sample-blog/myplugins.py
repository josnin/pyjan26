import os
import glob
from pyjan26.registry import register_custom_pages, register_custom_filters, register_custom_collections, register_post_build
from pyjan26.core import render_page, render_string, settings, get_output_directory, generate_file, copy_static_files

### START Custom collections ########
def sitemap_collections(collections):
    sitemap = []
    print('Building sitemap collections...')
    for sitemap_conf in settings.SITEMAP_CONFIG:
        for item in collections.get(sitemap_conf['collection']):
            permalink1 = item.get('permalink')
            out_dir2, final_out = get_output_directory(sitemap_conf['collection'], permalink1, None, item)

            loc = None
            if 'index' not in final_out:
                loc = f'{settings.SITE_NAME}/{final_out}'
            elif out_dir2:
                loc = f'{settings.SITE_NAME}/{out_dir2}/'

            if loc:
                sitemap.append({
                    'loc': loc,
                    'changefreq' : sitemap_conf['changefreq'],
                    'priority': sitemap_conf['priority']
                })

    return {'sitemap': sitemap }

def blog_collections(collections):
    print('Building blogs collections...')
    return {'blogs': list(filter(lambda post: post['name'] != 'index', collections.get('posts'))) }

def all_tags_collections(collections):
    #depdent on blog_collections
    print('Building all_tags collections...')
    return {'all_tags': list(tag for blog in collections.get('blogs') for tag in blog['tags'])}


#register custom collections
register_custom_collections([
    sitemap_collections,
    blog_collections,
    all_tags_collections
])
### END Custom collections ########



### START Custom filters ########
def filter_tag(value, tag_name):
    return list(filter(lambda val: tag_name in val['tags'], value))

#Register filters
register_custom_filters([
    filter_tag,
])
### END Custom filters ########


### START Custom Page #########
def repeat_page(*args, **kwargs):
    item, collection_name, collections, settings, permalink = args
    for data1 in collections.get(item.get('data')):
        item['page_items'] = data1
        page_data = {
            'collection_name': collection_name, 
            'collections': collections,  
            'settings': settings, 
            'items': item,
            'permalink2': f'{data1}/'
        }
        render_page(page_data)

    return { 'skip_next': True }

def sitemap_page(*args, **kwargs):
    item, collection_name, collections, _, permalink = args

    # Render Markdown XML content
    xml_content = render_string(
            item['content'], 
            { 'collections': collections }
        )

    final_out = os.path.join(settings.OUTPUT_DIR, 'sitemap.xml')
    print(f'Generating page at {final_out}')
    generate_file(f'{settings.OUTPUT_DIR}/', final_out, xml_content)

    return { 'skip_next': True }

#Register the custom page
register_custom_pages([repeat_page, sitemap_page])

### END Custom Page #########


### START Post build ########
import sass
def scss_to_css():
    for pattern in settings.CSS_SCSS_PATTERNS:
        scss_files = glob.glob(os.path.join(settings.CONTENT_DIR, pattern))
        for scss_file in scss_files:
            with open(scss_file, 'r') as file:
                scss_content = file.read()

            #convert scss to css using libsass
            css_content = sass.compile(string=scss_content, output_style='expanded')

            css_file = f'{os.path.splitext(scss_file)[0]}.css'

            #write the scss content to output file
            with open(css_file, 'w') as file:
                file.write(css_content)
        
            print(f'SCSS generated at {css_file}')

    #TODO how to exclude scss file on public? 
    copy_static_files(settings.STATIC_PATHS, settings.OUTPUT_DIR)

register_post_build([scss_to_css])
### END Post build ########