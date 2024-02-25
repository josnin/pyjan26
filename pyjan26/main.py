import os
import shutil
import pkg_resources
from importlib import import_module
from pyjan26.core import Jan26Gen


def generate_file(file_path: str, default_file: str) -> None:

    if not os.path.exists(file_path):
        default_path = pkg_resources.resource_filename(__name__, default_file)
        shutil.copy(default_path, file_path)
        print(f"Created {file_path} from {default_path}")

if __name__ == '__main__':

    generate_file('custom_pages.py', 'default_custom_pages.py')
    generate_file('custom_collections.py', 'default_custom_collections.py')
    generate_file('custom_filters.py', 'default_custom_filters.py')

    custom_pages_module = os.environ.setdefault('PYJAN26_PAGES_MODULE', 'custom_pages')
    collections_module = os.environ.setdefault('PYJAN26_COLLECTIONS_MODULE', 'custom_collections')
    filters_module = os.environ.setdefault('PYJAN26_FILTERS_MODULE', 'custom_filters')

    import_module(custom_pages_module) # type: ignore
    import_module(collections_module) # type: ignore
    import_module(filters_module) # type: ignore

    gen = Jan26Gen()
    gen.generate_site()

