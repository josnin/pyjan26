---
title: "First Blog Post"
description: This is an example blog post for Python
date: 2024-01-21
tags: ["python"]
---

# First Blog

First Blog content

```python
### START Custom filters ########
def filter_tag(value, tag_name):
    return list(filter(lambda val: tag_name in val['tags'], value))

#Register filters
register_custom_filters([
    filter_tag,
])
```


