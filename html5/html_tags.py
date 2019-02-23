class Tag:
    TAG = 'tag_name'
    attributes = {}
    REQUIRED_ATTRIBUTES = {}
    SUB_TAGS = frozenset(('title', 'style', 'base', 'link', 'meta', 'script', 'noscript'))
    END_TAG = False
