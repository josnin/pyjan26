import os
from pyjan26.core import Jan26Gen
from importlib import import_module

custom_pages_module = os.environ.get('PYJAN26_PAGES_MODULE')
if not custom_pages_module:
    print("PYJAN26_PAGES_MODULE environment variable is not set")
else:
    custom_pages = import_module(custom_pages_module) # type: ignore
    

collections_module = os.environ.get('PYJAN26_COLLECTIONS_MODULE')
if not collections_module:
    print("PYJAN26_COLLECTIONS_MODULE environment variable is not set")
else:
    custom_collections = import_module(collections_module) # type: ignore


filters_module = os.environ.get('PYJAN26_FILTERS_MODULE')
if not filters_module:
    print("PYJAN26_FILTERS_MODULE environment variable is not set")
else:
    custom_filters = import_module(filters_module) # type: ignore


if __name__ == '__main__':

    gen = Jan26Gen()
    gen.generate_site()

