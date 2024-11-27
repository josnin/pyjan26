import os
import glob
from pyjan26.registry import register_custom_pages, register_custom_filters, register_custom_collections
from pyjan26.core import render_page, render_string, settings

### START Custom collections ########
def blog_collections(collections):
    print('Building blogs collections...')
    return {'blogs': list(filter(lambda post: post['name'] != 'index', collections.get('posts'))) }

def all_tags_collections(collections):
    #depdent on blog_collections
    print('Building all_tags collections...')
    return {'all_tags': list(tag for blog in collections.get('blogs') for tag in blog['tags'])}


#register custom collections
register_custom_collections([
    blog_collections,
    all_tags_collections
])
### END Custom collections ########



### START Custom filters ########
def filter_tag(value, tag_name):
    return list(filter(lambda val: tag_name in val['tags'], value))

#Register filters
register_custom_filters([
    filter_tag,
])
### END Custom filters ########

