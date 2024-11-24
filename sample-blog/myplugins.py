import os
import glob
from pyjan26.registry import register_custom_pages, register_custom_filters, register_custom_collections
from pyjan26.core import render_page, render_string, settings, get_output_directory, generate_file

### START Custom collections ########
def sitemap_collections(collections):
    sitemap = []
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
    return {'blogs': list(filter(lambda post: post['name'] != 'index', collections.get('posts'))) }

def all_tags_collections(collections):
    #depdent on blog_collections
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
    generate_file(f'{settings.OUTPUT_DIR}/', final_out, xml_content)
    print(f'RENDER SITEMAP_PAGE: output file {final_out}')

    return { 'skip_next': True }

#Register the custom page
register_custom_pages([repeat_page, sitemap_page])

### END Custom Page #########