from typing import List, Dict, Any, Union, Callable, Tuple

CUSTOM_PAGE_REGISTRY = {}
CUSTOM_FILTER_REGISTRY = []
CUSTOM_COLLECTION_REGISTRY = []

def register_custom_filters(custom_function: List[Callable]) -> None:
    CUSTOM_FILTER_REGISTRY.extend(custom_function)

def register_custom_collections(custom_function: List[Callable]) -> None:
    CUSTOM_COLLECTION_REGISTRY.extend(custom_function)

def register_custom_page(name, func) -> None:
    CUSTOM_PAGE_REGISTRY[name] = func
    
def get_custom_page(name):
    return CUSTOM_PAGE_REGISTRY.get(name)