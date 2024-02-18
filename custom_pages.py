from generator import render_page, render_string

def custom_page1(*args, **kwargs):
    print('calling custom page1')

    import pprint
    item, collection_name, collections, settings = args
    out_dir = kwargs.get('out_dir')
    out_dir =  render_string(out_dir, item)

    page_data = {
        'collection_name': collection_name,
        'collections': collections,
        'items': item,
        'out_dir': out_dir
    }

    render_page(page_data)

    return { 'skip_next': False }

def render_split_by_items(self, items, collection_name, collections, settings2, out_dir=None):
    split_by = items.get('split_by')
    split_by_items = split_by.get('items')
    alias = split_by.get('alias', f'splitby{collection_name.title()}')

    for page_items in collections.get(split_by_items):
        #out_dir1 = self.render_output_directory(out_dir, page_items)
        out_dir1 =  render_string(out_dir, page_item)
        #out_dir1 = render_output_directory(out_dir, page_items)
        print(page_items, out_dir)
        page_data = {
            'collection_name': collection_name,
            'collections': collections,
            'settings': settings2,
            'items': items,
            'page_items': page_items, 
            'alias': alias,
            'out_dir': out_dir1
        }

        #if settings.DEBUG:
        #    print(f'RENDER_SPLIT_BY: page_data: {page_data}')

        self.render_page(page_data, 1)
