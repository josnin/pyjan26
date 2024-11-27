import os
import glob
from pyjan26.registry import register_custom_pages, register_custom_collections
from pyjan26.core import render_string, settings, get_output_directory, generate_file

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

#register custom collections
register_custom_collections([
    sitemap_collections,
])
### END Custom collections ########


### START Custom Page #########
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
register_custom_pages([sitemap_page])

### END Custom Page #########

