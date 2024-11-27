from pyjan26.registry import register_custom_pages
from pyjan26.core import render_page

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

#Register the custom page
register_custom_pages([repeat_page])

### END Custom Page #########

