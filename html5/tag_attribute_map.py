from html_attributes_global import GLOBAL_ATTRIBUTE_BY_NAME

ATTRIBUTES_FOR_ALL_TAGS = GLOBAL_ATTRIBUTE_BY_NAME.keys() + {'oncontextmenu'}

ATTRIBUTE_TAG_INCLUDE = {
    'onafterprint': {'body'},
    'onbeforeprint': {'body'},
    'onbeforeunload': {'body'},
    'onerror': {'body'},
    'onhashchange': {'body'},
    'onload': {'body'},
    'onmessage': {'body'},
    'onoffline': {'body'},
    'ononline': {'body'},
    'onpagehide': {'body'},
    'onpageshow': {'body'},
    'onpopstate': {'body'},
    'onresize': {'body'},
    'onstorage': {'body'},
    'onunload': {'body'},

    'onchange': {'select', 'textarea'},
    'oninput': {'textarea'},
    'oninvalid': {'input'},
    'onreset': {'form'},
    'onselect': {'textarea'},
    'onsubmit': {'form'},

    'onscroll': {'address', 'blockquote', 'body', 'caption', 'center', 'dd', 'dir', 'div', 'dl', 'dt', 'fieldset', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'html', 'li', 'menu', 'object', 'ol', 'p', 'pre', 'select', 'tbody', 'textarea', 'tfoot', 'thead', 'ul'},

    'ontoggle': {'details'},
}

ATTRIBUTE_TAG_EXCLUDE = {
    'onblur': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onfocus': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},

    'onkeydown': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onkeypress': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onkeyup': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},

    'onclick': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'ondblclick': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onmousedown': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onmousemove': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onmouseout': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onmouseover': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
    'onmouseup': {'base', 'bdo', 'br', 'head', 'html', 'iframe', 'meta', 'param', 'script', 'style', 'title'},
}


def verify(tag, attribute):
    # TODO: == '' -> isinstance

    if tag.TAG == '!--':
        return False

    if tag.TAG == '!DOCTYPE':
        return attribute.ATTR == 'html'

    if tag.TAG in frozenset(('html', 'head', 'title')):
        return attribute.ATTR in GLOBAL_ATTRIBUTE_BY_NAME

    if attribute.ATTR == 'cite':
        return tag.TAG in frozenset(('blockquote', 'del', 'ins',))

    if attribute.ATTR == 'datetime':
        return tag.TAG in frozenset(('del', 'ins',))

    if attribute.ATTR in ATTRIBUTES_FOR_ALL_TAGS:
        return True

    if tag.TAG in ATTRIBUTE_TAG_INCLUDE.get(attribute.ATTR, {}):
        return True

    if tag.TAG == 'input':
        type_content = tag.attributes.get('type', '')
        if type_content:
            if attribute.ATTR == 'onchange' and type_content in {
                    'checkbox', 'file', 'password', 'radio', 'range', 'search', 'text'
            }:
                return True
            if attribute.ATTR == 'oninput' and type_content in {'password', 'search', 'text'}:
                return True
            if attribute.ATTR == 'onsearch' and type_content == 'search':
                return True
            if attribute.ATTR == 'onselect' and type_content in {'file', 'password', 'text'}:
                return True

    if tag.TAG not in ATTRIBUTE_TAG_EXCLUDE.get(attribute.ATTR, {}):
        return True

    return False
