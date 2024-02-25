from pyjan26.registry import register_custom_filters

# Define custom filter functions
def custom_filter_function1(value):
    # Custom filter logic
    return f"{value} customize??" 

def custom_filter_function2(value):
    # Custom filter logic
    pass

register_custom_filters([
    custom_filter_function1,
    custom_filter_function2
])