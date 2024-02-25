from pyjan26.registry import register_custom_collections

def tag_list(collections):
    #pprint.pprint(collections)
    return {'tags': [{ 'tag': 'javascript'}, {'tag': 'python' }] }


register_custom_collections([
    tag_list
])