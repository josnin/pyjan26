from pyjan26.registry import register_custom_filters

def capitalize_words(value):
    return ' '.join(word.capitalize() for word in value.split())


register_custom_filters([
    capitalize_words,
])