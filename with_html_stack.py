#!/usr/bin/env python3

from typing import Optional, List


def from_safe_name(name, safe_prefix='_'):
    if name.startswith(safe_prefix):
        return name[len(safe_prefix):].replace('_', '-')
    return name


class TextParams:

    def __init__(self, level=0, offset=' ' * 4, newline='\n'):
        self.level = level
        self.offset = offset
        self.newline = newline

    @property
    def indent(self):
        return self.level * self.offset

    @property
    def inner(self):
        return TextParams(self.level + 1, self.offset, self.newline)

    def line(self, middle, indent=None):
        if indent is None:
            return self.indent + middle + self.newline
        return indent + middle + self.newline


DEV_PARAMS = TextParams()
PROD_PARAMS = TextParams(offset='', newline='')


class HTMLRaw:

    def __init__(self, raw, prefix=None, suffix=None):
        self.raw = raw
        self.prefix = prefix
        self.suffix = suffix

    def text(self, params):
        lines = self.raw.splitlines()

        spaces = 0
        while lines[0][spaces].isspace():
            spaces += 1
        old_indent = lines[0][:spaces]

        result = ''
        for item in lines:
            if item.startswith(old_indent):
                tail = item[len(old_indent):]
                new_indent = params.indent
            else:
                tail = item
                new_indent = ''

            if self.prefix:
                tail = self.prefix + tail
            if self.suffix:
                tail += self.suffix

            result += params.line(tail, indent=new_indent)
        return result


class HTMLComment(HTMLRaw):

    def __init__(self, raw):
        super().__init__(raw, prefix='<!-- ', suffix=' -->')


class HTMLAttribute:

    def __init__(self, attribute, value=None):
        self.attribute = from_safe_name(attribute)
        self.value = value  # use html.escape(value) for value if you need it

    def text(self):
        if self.value is None:
            return self.attribute
        return '{}="{}"'.format(self.attribute, self.value)


class HTMLTag:

    def __init__(self, name, **kwargs):
        self.name = from_safe_name(name)
        self.attributes = [HTMLAttribute(k, v) for k, v in kwargs.items()]

    def text_attributes(self):
        ret = ' '.join([x.text() for x in self.attributes])
        if ret:
            ret = ' ' + ret
        return ret

    def text(self, params, raw: Optional[str] = None) -> str:
        prefix = '<{}{}'.format(self.name, self.text_attributes())
        ret = params.line('<{}{}>'.format(self.name, self.text_attributes()))

        if self.name.startswith('!'):
            if raw is not None:
                raise RuntimeError('there may be no HTML in tag name starting with "!"')
            return params.line(prefix + '>')

        if raw is None:
            return params.line(prefix + '/>')

        ret = params.line(prefix + '>')
        ret += raw
        ret += params.line('</{}>'.format(self.name))
        return ret


class HTMLNode:

    def __init__(self,
                 parent: Optional['HTMLNode'] = None,
                 raw: Optional[HTMLRaw] = None,
                 tag: Optional[HTMLTag] = None) -> None:
        self.parent = parent    # None here means root node
        self.node_raw = raw
        self.node_tag = tag
        self.children: List[HTMLNode] = []

    def root(self):
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    def verify(self):
        if not (self.parent is None or isinstance(self.parent, HTMLNode)):
            raise RuntimeError('HTMLNode instance or None expected as "parent" parameter value')
        if not (self.node_raw is None or isinstance(self.node_raw, HTMLRaw)):
            raise RuntimeError('HTMLRaw instance expected as "raw" parameter value')
        if not (self.node_tag is None or isinstance(self.node_tag, HTMLTag)):
            raise RuntimeError('HTMLTag instance expected as "tag" parameter value')

        if self.node_raw is not None and self.children:
            raise RuntimeError("node can't contain HTML and children nodes at the same time")

    def text(self, params):
        self.verify()

        children_params = params if self.node_tag is None else params.inner
        if self.children:
            children_raw = ''.join(x.text(children_params) for x in self.children)
        elif self.node_raw is not None:
            children_raw = self.node_raw.text(children_params)
        else:
            children_raw = None

        if self.node_tag is None:
            return children_raw
        return self.node_tag.text(params, children_raw)


class HTMLDocument:
    """
    Example:
    ---
    from with_html_stack import HTMLDocument


    H = HTMLDocument()
    H.tag('!doctype', html=None)
    with H.tag('html', lang='en'):
        with H.tag('head'):
            H.tag('title', raw='Example Domain')
            H.tag('meta', charset='utf-8')
        with H.tag('body'):
            with H.tag('div'):
                H.tag('h1', raw='Example Domain')
                with H.tag('p'):
                    H.raw('This domain is for use in illustrative examples in documents. You ')
                    H.raw('may use this domain in literature without prior coordination or asking for permission.')
                with H.tag('p'):
                    with H.tag('a', href='https://www.iana.org/domains/example'):
                        H.raw('More information')
    html = H.text(PROD_PARAMS)
    """

    def __init__(self) -> None:
        self.node = HTMLNode()

    def raw(self, raw: str) -> None:
        self.node.children.append(HTMLNode(
            parent=self.node,
            raw=HTMLRaw(raw),
            tag=None,
        ))

    def comment(self, raw: str) -> None:
        self.node.children.append(HTMLNode(
            parent=self.node,
            raw=HTMLComment(raw),
            tag=None,
        ))

    def tag(self, name: str, raw: Optional[str] = None, **kwargs) -> None:
        self.node.children.append(HTMLNode(
            parent=self.node,
            raw=None if raw is None else HTMLRaw(raw),
            tag=HTMLTag(name, **kwargs),
        ))
        return self

    def __enter__(self):
        if not self.node.children:
            raise RuntimeError('no child node')
        if self.node.children[-1].node_tag is None:
            raise RuntimeError('only node with tag can be used as context manager')
        self.node = self.node.children[-1]

    def __exit__(self, exc_type, exc_value, traceback):
        if self.node.parent is None:
            raise RuntimeError('__enter__ not called')
        self.node = self.node.parent

    def text(self, params):
        return self.node.root().text(params)
