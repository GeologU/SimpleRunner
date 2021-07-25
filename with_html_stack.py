#!/usr/bin/env python3

import copy
import html
from typing import List, Optional

_INDENT_ATOM = "    "  # 4 spaces
_UNSAFE_NAMES = {"id"}
_SAFE_PREFIX = "_"
_DEFAULT_X_FIX = ""


def to_safe_name(name: str, safe_prefix: str = _SAFE_PREFIX) -> str:
    if name in _UNSAFE_NAMES:
        return safe_prefix + name
    snake = name.replace("-", "_")
    if snake != name:
        return safe_prefix + snake
    return name


def from_safe_name(name: str, safe_prefix: str = _SAFE_PREFIX) -> str:
    if name.startswith(safe_prefix):
        return name[len(safe_prefix) :].replace("_", "-")
    return name


def html_as_code(data: Optional[str]) -> str:
    if data is None:
        return "None"
    unescaped = html.unescape(data)
    if unescaped != data:
        return "html.escape(" + repr(unescaped) + ")"
    return repr(data)


def get_indent(line: str) -> str:
    spaces = 0
    for symbol in line:
        if not symbol.isspace():
            break
        spaces += 1
    return line[:spaces]


class TextParams:
    def __init__(self, level: int = 0, offset: str = _INDENT_ATOM, newline: str = "\n"):
        self.level: int = level
        self.offset: str = offset
        self.newline: str = newline

    def __str__(self) -> str:
        # explicit "repr" below in order to show escaped symbols like \n correctly
        return f"TextParams(level={self.level}, offset={repr(self.offset)}, newline={repr(self.newline)})"

    @property
    def indent(self) -> str:
        return self.level * self.offset

    @property
    def inner(self) -> "TextParams":
        return TextParams(self.level + 1, self.offset, self.newline)

    def line(self, middle: str, indent: Optional[str] = None) -> str:
        if indent is None:
            return self.indent + middle + self.newline
        return indent + middle + self.newline

    def text(
        self, lines: List[str], prefix: Optional[str] = _DEFAULT_X_FIX, suffix: Optional[str] = _DEFAULT_X_FIX
    ) -> str:
        """
        Return text with lines shifted according to indent.
        Existing shortest indent will be removed from all lines in case all of them start with it.
        """
        if not lines:
            return ""

        if prefix is None:
            prefix = _DEFAULT_X_FIX
        if suffix is None:
            suffix = _DEFAULT_X_FIX

        indents = {x: get_indent(x) for x in lines}
        min_indent = min(indents.values(), key=len)
        min_is_common = min_indent and all(x.startswith(min_indent) for x in lines)

        result = ""
        for item in lines:
            item_indent = indents[item][len(min_indent) :] if min_is_common else indents[item]
            result += self.line(item_indent + prefix + item[len(indents[item]) :] + suffix)
        return result


DEV_PARAMS = TextParams()
PROD_PARAMS = TextParams(offset="", newline="")


class HTMLRaw:
    def __init__(self, raw, prefix=_DEFAULT_X_FIX, suffix=_DEFAULT_X_FIX):
        self.raw = raw
        self.prefix = prefix
        self.suffix = suffix

    def text(self, params: TextParams):
        lines = self.raw.splitlines()
        return params.text(lines, self.prefix, self.suffix)

    def code(self, params: TextParams) -> str:
        prefix_suffix = ""
        if self.prefix != _DEFAULT_X_FIX:
            prefix_suffix += ", prefix={}".format(html_as_code(self.prefix))
        if self.suffix != _DEFAULT_X_FIX:
            prefix_suffix += ", suffix={}".format(html_as_code(self.suffix))
        return params.line("doc.raw({}{})".format(html_as_code(self.raw), prefix_suffix))


class HTMLComment(HTMLRaw):
    def __init__(self, raw):
        super().__init__(raw, prefix="<!-- ", suffix=" -->")

    def code(self, params: TextParams) -> str:
        return params.line("doc.comment({})".format(html_as_code(self.raw)))


class HTMLAttribute:
    def __init__(self, attribute, value=None, escape=False):
        self.attribute = from_safe_name(attribute)
        self.value = html.escape(value) if (escape and value is not None) else value

    def text(self):
        if self.value is None:
            return self.attribute
        return '{}="{}"'.format(self.attribute, self.value)

    def code(self) -> str:
        return to_safe_name(self.attribute) + "=" + html_as_code(self.value)


class HTMLTag:
    def __init__(self, name, **kwargs):
        self.name = from_safe_name(name)
        self.attributes = [HTMLAttribute(k, v) for k, v in kwargs.items()]

    def text_attributes(self):
        ret = " ".join([x.text() for x in self.attributes])
        if ret:
            ret = " " + ret
        return ret

    def text(self, params: TextParams, raw: Optional[str] = None) -> str:
        prefix = "<{}{}".format(self.name, self.text_attributes())

        if self.name.startswith("!"):
            if raw is not None:
                raise RuntimeError('there may be no HTML in tag name starting with "!"')
            return params.line(prefix + ">")

        if raw is None:
            return params.line(prefix + "/>")

        ret = params.line(prefix + ">")
        ret += raw
        if params.newline and not ret.endswith(params.newline):
            ret += params.newline
        ret += params.line("</{}>".format(self.name))
        return ret

    def code_attributes(self):
        ret = ", ".join([x.code() for x in self.attributes])
        if ret:
            ret = ", " + ret
        return ret

    def code(self, params: TextParams, raw: Optional[str] = None, with_statement: bool = False) -> str:
        safe_name = to_safe_name(self.name)
        prefix = "doc(" + html_as_code(safe_name) + self.code_attributes()

        if self.name.startswith("!"):
            if raw is not None:
                raise RuntimeError('there may be no HTML in tag name starting with "!"')
            return params.line(prefix + ")")

        if raw is None:
            return params.line(prefix + ")")

        if not with_statement:
            return params.line(prefix + ", raw=" + html_as_code(raw) + ")")

        ret = params.line("with " + prefix + "):")
        ret += raw
        if params.newline and not ret.endswith(params.newline):
            ret += params.newline
        return ret


class HTMLNode:
    def __init__(
        self, parent: Optional["HTMLNode"] = None, raw: Optional[HTMLRaw] = None, tag: Optional[HTMLTag] = None
    ) -> None:
        self.parent = parent  # None here means root node
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

        for item in self.children:
            if not isinstance(item, HTMLNode):
                raise RuntimeError("HTMLNode instance expected as children item")

    def text(self, params: TextParams):
        self.verify()

        children_params = params if self.node_tag is None else params.inner
        children_raw: Optional[str]
        if self.children:
            children_raw = "".join(x.text(children_params) for x in self.children)
        elif self.node_raw is not None:
            children_raw = self.node_raw.text(children_params)
        else:
            children_raw = None

        if self.node_tag is None:
            result = children_raw
        else:
            result = self.node_tag.text(params, children_raw)
        return result if result is not None else ""

    def code(self, params: TextParams):
        self.verify()

        with_statement = bool(params.newline)

        children_params = params if self.node_tag is None else params.inner
        children_raw: Optional[str]
        if self.children:
            children_raw = "".join(x.code(children_params) for x in self.children)
        elif self.node_raw is not None:
            if with_statement:
                children_raw = self.node_raw.code(children_params)
            else:
                children_raw = self.node_raw.text(children_params)
        else:
            children_raw = None

        if self.node_tag is None:
            result = children_raw
        else:
            result = self.node_tag.code(params, children_raw, with_statement=with_statement)
        return result if result is not None else ""


class HTMLDocument:
    """Example:

    >>> from with_html_stack import HTMLDocument, DEV_PARAMS, PROD_PARAMS
    >>> doc = HTMLDocument(doctype=False)
    >>> doc('!DOCTYPE', html=None)      # doctest: +ELLIPSIS
    <with_html_stack.HTMLDocument object at 0x...>
    >>> with doc('html', lang='en'):    # doctest: +ELLIPSIS
    ...     with doc('head'):
    ...             doc('title', raw='Example Domain')
    ...             doc('meta', charset='utf-8')
    ...     with doc('body'):
    ...             with doc('div'):
    ...                     doc('h1', raw='Example Domain')
    ...                     with doc('p'):
    ...                             doc.raw('This domain is for use in illustrative examples in documents. You ')
    ...                             doc.raw('may use this domain in literature without prior coordination or asking for permission.')
    ...                     with doc('p'):
    ...                             with doc('a', href='https://www.iana.org/domains/example'):
    ...                                     doc.raw('More information')
    ...
    <with_html_stack.HTMLDocument object at 0x...>
    <with_html_stack.HTMLDocument object at 0x...>
    <with_html_stack.HTMLDocument object at 0x...>

    >>> print(doc.text(DEV_PARAMS))
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <title>
                Example Domain
            </title>
            <meta charset="utf-8"/>
        </head>
        <body>
            <div>
                <h1>
                    Example Domain
                </h1>
                <p>
                    This domain is for use in illustrative examples in documents. You
                    may use this domain in literature without prior coordination or asking for permission.
                </p>
                <p>
                    <a href="https://www.iana.org/domains/example">
                        More information
                    </a>
                </p>
            </div>
        </body>
    </html>
    <BLANKLINE>

    >>> print(doc.text(PROD_PARAMS))
    <!DOCTYPE html><html lang="en"><head><title>Example Domain</title><meta charset="utf-8"/></head><body><div><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p><p><a href="https://www.iana.org/domains/example">More information</a></p></div></body></html>
    """

    def __init__(self, doctype: bool = True) -> None:
        self.node = HTMLNode()
        if doctype:
            self("!DOCTYPE", html=None)

    def raw(self, raw: str) -> None:
        self.node.children.append(
            HTMLNode(
                parent=self.node,
                raw=HTMLRaw(raw),
                tag=None,
            )
        )

    def comment(self, raw: str) -> None:
        self.node.children.append(
            HTMLNode(
                parent=self.node,
                raw=HTMLComment(raw),
                tag=None,
            )
        )

    def __call__(self, name: str, raw: Optional[str] = None, **kwargs) -> "HTMLDocument":
        # It is more clear to write
        #   doc.add_tag(tag_name, ...)
        # but usually there are a lot of tags in the document, so that use
        #   doc(tag_name, ...)
        # to reduce repetitive text.
        self.node.children.append(
            HTMLNode(
                parent=self.node,
                raw=None if raw is None else HTMLRaw(raw),
                tag=HTMLTag(name, **kwargs),
            )
        )
        return self  # for use in "with" statement

    def __enter__(self):
        if not self.node.children:
            raise RuntimeError("no child node")
        if self.node.children[-1].node_tag is None:
            raise RuntimeError("only node with tag can be used as context manager")
        self.node = self.node.children[-1]

    def __exit__(self, exc_type, exc_value, traceback):
        if self.node.parent is None:
            raise RuntimeError("__enter__ not called")
        self.node = self.node.parent

    def append(self, other: "HTMLDocument", deepcopy: bool = False) -> None:
        self.node.children.append(copy.deepcopy(other.node) if deepcopy else other.node)

    def text(self, params: TextParams) -> str:
        return self.node.root().text(params)

    def code(self) -> str:
        return self.node.root().code(DEV_PARAMS)

    def content(self, params: TextParams = PROD_PARAMS, coding: str = "UTF-8") -> bytes:
        return bytes(self.text(params), coding)
