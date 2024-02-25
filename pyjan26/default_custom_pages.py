
from pyjan26.registry import register_custom_page
from pyjan26.core import render_page, render_string

#Example 

##Create a custom page function
#def custom_page1(*args, **kwargs):
#    
#
#    item, collection_name, collections, settings = args
#    out_dir = kwargs.get('out_dir')
#
#    # render jinja variable
#    if out_dir:
#        out_dir =  render_string(out_dir, item)
#
#    page_data = {
#        'collection_name': collection_name,
#        'collections': collections,
#        'items': item,
#        'out_dir': out_dir
#    }
#
#    render_page(page_data)
#
#    return { 'skip_next': False }
#
#
##Register the custom page
#register_custom_page('jump', custom_page1)