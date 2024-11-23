import os
import glob
from pyjan26.registry import register_custom_pages, register_custom_filters, register_custom_collections
from pyjan26.core import render_page, render_string, settings, get_output_directory, generate_file

#START --- Custom collections
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
#END --- Custom collections





#START --- Custom filters
def filter_tag(value, tag_name):
    return list(filter(lambda val: tag_name in val['tags'], value))

#Register filters
register_custom_filters([
    filter_tag,
])
#END --- Custom filters


#START --- Custom Page
#Example 

## The use case of custom_page function includes scenarios where you need to 
## generate pages dynamically based on data from an external API, database, 
## or any other data source, or when you want to programmatically 
## generate pages based on specific criteria or conditions that 
## cannot be achieved through standard file-based page generation.
def repeat_page(*args, **kwargs):

    item, collection_name, collections, settings, permalink = args

    for data1 in collections.get(item.get('data')):
        permalink2 = None
        if permalink:
            permalink2 =  render_string(permalink, { 'tag': data1 } )

        item['page_items'] = data1

        page_data = {
            'collection_name': collection_name, 
            'collections': collections,  
            'settings': settings, 
            'items': item,
            'permalink2': permalink2
        }

        render_page(page_data)

    return { 'skip_next': True }

def sitemap_page(*args, **kwargs):

    item, collection_name, collections, _, permalink = args

    # Render Markdown HTML content
    html_content = render_string(
            item['content'], 
            { 'collections': collections }
        )
    
    out_dir2 = f'{settings.OUTPUT_DIR}/'
    final_out = os.path.join(settings.OUTPUT_DIR, 'sitemap.xml')

    print(f'RENDER_PAGE: output_dir {out_dir2}  output file {final_out}')
    generate_file(out_dir2, final_out, html_content)

    return { 'skip_next': True }




#Register the custom page
register_custom_pages([repeat_page, sitemap_page])

#END --- Custom Page