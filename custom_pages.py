
from pyjan26.registry import register_custom_page
from pyjan26.core import render_page, render_string

# The use case of custom_page function includes scenarios where you need to 
# generate pages dynamically based on data from an external API, database, 
# or any other data source, or when you want to programmatically 
# generate pages based on specific criteria or conditions that 
# cannot be achieved through standard file-based page generation.
def custom_page1(*args, **kwargs):
    

    item, collection_name, collections, settings = args
    out_dir = kwargs.get('out_dir')

    # render jinja variable
    if out_dir:
        out_dir =  render_string(out_dir, item)

    page_data = {
        'collection_name': collection_name,
        'collections': collections,
        'items': item,
        'out_dir': out_dir
    }

    render_page(page_data)

    return { 'skip_next': False }


register_custom_page('custom1', custom_page1)