from pyjan26.core import Jan26Gen
#import os
#
#def get_custom_collections_fn():
#    res = None
#
#    #import custom_collections
#    from importlib import import_module
#    collections_module = os.environ.get('PYJAN26_COLLECTIONS_MODULE')
#    if not collections_module:
#        print("PYJAN26_COLLECTIONS_MODULE environment variable is not set")
#    else:
#        custom_collections = import_module(collections_module) # type: ignore
#
#        # Get all function names from the module
#        function_names = [name for name in dir(custom_collections) if callable(getattr(custom_collections, name))]
#
#        # Get the function objects using getattr() and pass them to add_collections
#        res = [getattr(custom_collections, name) for name in function_names]
#
#    return res
#
#def get_custom_filters_fn():
#    res = None
#
#    #import custom_filters
#    from importlib import import_module
#    filters_module = os.environ.get('PYJAN26_FILTERS_MODULE')
#    if not filters_module:
#        print("PYJAN26_FILTERS_MODULE environment variable is not set")
#    else:
#        custom_filters = import_module(filters_module) # type: ignore
#
#        # Get all function names from the module
#        function_names = [name for name in dir(custom_filters) if callable(getattr(custom_filters, name))]
#
#        # Get the function objects using getattr() and pass them to add_filters
#        res = [getattr(custom_filters, name) for name in function_names]
#    
#    return res

if __name__ == '__main__':

    gen = Jan26Gen()
    gen.generate_site()

