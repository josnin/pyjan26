from pyjan26.registry import register_custom_collections

def custom_collection_function1(collections):
    # Logic to generate collection 1
    return {'collection1': [{'metadata': {}, 'content': 'Content 1'}, {'metadata': {}, 'content': 'Content 2'}]}

def custom_collection_function2(collections):
    #print(collections)
    # Logic to generate collection 2
    return {'collection2': [{'metadata': {}, 'title': 'Custom Collections 1'}, {'metadata': {}, 'title': 'Custom Collections 2'}]}


register_custom_collections([
    custom_collection_function1,
    custom_collection_function2
])