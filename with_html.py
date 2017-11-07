#!/usr/bin/env python3

from functools import partialmethod


class TextParams():

    def __init__(self, level=0, offset='    ', newline='\n'):
        self.level = level
        self.offset = offset
        self.newline = newline

    def indent(self):
        return self.level * self.offset

    def inner(self):
        return TextParams(self.level + 1, self.offset, self.newline)

    def outer(self):
        return TextParams(
            self.level - 1 if self.level else self.level,
            self.offset,
            self.newline
        )


class HTMLRaw():

    def __init__(self, mode, raw):
        self.mode = mode
        self.raw = raw

    def text(self, params):
        if self.mode == 'continuation':
            return self.raw
        elif self.mode == 'line':
            return params.indent() + self.raw + params.newline
        elif self.mode == 'block':
            lines = self.raw.splitlines()

            spaces = 0
            while lines[0][spaces].isspace():
                spaces += 1
            prefix = lines[0][:spaces]

            # don't change some special indent, if any
            new_lines = []
            for item in lines:
                if item.startswith(prefix):
                    new_lines.append(params.indent() + item[len(prefix):])
                else:
                    new_lines.append(item)
            return params.newline.join(new_lines) + params.newline
        else:
            raise RuntimeError('wrong mode: ' + self.mode)


class HTMLAttribute():

    def __init__(self, attribute, value=None):
        if attribute.startswith('xx'):
            self.attribute = attribute[len('xx'):].replace('_', '-')
        else:
            self.attribute = attribute

        self.value = value  # use html.escape(value) for value if you need it

    def text(self):
        if self.value is None:
            return self.attribute
        return '{}="{}"'.format(self.attribute, self.value)


class HTMLTag():

    def __init__(self, mode, name, **kwargs):
        self.mode = mode
        self.name = name
        self.attributes = [HTMLAttribute(k, v) for k, v in kwargs.items()]

    def text_attributes(self):
        ret = ' '.join([x.text() for x in self.attributes])
        if ret:
            ret = ' ' + ret
        return ret

    def text(self, params, raw):
        """
        Support several modes for greater clarity of final html:
        - no html in tag:
            <hr>
        - one-line tag with and without intendation before openning tag:
            <a href="http://example.com/">link</a>
            <p>This is a <a href="http://example.com/">link</a></p>
        - openning tag, html and closing tag are on separate lines:
            <a href="http://example.com/">
                link
            </a>
        """

        raw_attributes = self.text_attributes()

        if self.mode in ['continuation', 'line']:
            if raw is None:
                if self.name.startswith('!'):
                    ret = '<{name}{attrs}>'.format(name=self.name, attrs=raw_attributes)
                else:
                    ret = '<{name}{attrs} />'.format(name=self.name, attrs=raw_attributes)
            else:
                ret = '<{name}{attrs}>{raw}</{name}>'.format(
                    name=self.name, attrs=raw_attributes, raw=raw
                )
            if self.mode == 'line':
                ret = params.indent() + ret + params.newline
        elif self.mode == 'block':
            ret = '{indent}<{name}{attrs}>{newline}'.format(
                indent=params.indent(),
                name=self.name,
                attrs=raw_attributes,
                newline=params.newline,
            )
            if raw is not None:
                ret += raw
            ret += '{indent}</{name}>{newline}'.format(
                indent=params.indent(),
                name=self.name,
                newline=params.newline,
            )
        else:
            raise RuntimeError('wrong mode: ' + self.mode)

        return ret


class HTMLNode:

    def __init__(self, parent=None, tag=None, raw=None):
        self.parent = parent
        self.children = []
        self.node_tag = tag
        self.node_raw = raw

    def text_children(self, params):
        if self.children:
            return ''.join([x.text(params) for x in self.children])
        return None

    def text(self, params):
        if self.node_tag is None:
            if self.node_raw is None:
                return self.text_children(params)
            else:
                assert not self.children
                return self.node_raw.text(params)
        else:
            if self.node_raw is None:
                raw = self.text_children(params.inner())
            else:
                assert not self.children
                raw = self.node_raw.text(params.inner())
            return self.node_tag.text(params, raw)

    def tag(self, mode, name, raw=None, **kwargs):
        raw_mode = 'continuation' if mode in ['continuation', 'line'] else mode
        n = HTMLNode(
            self,
            tag=HTMLTag(mode, name, **kwargs),
            raw=None if raw is None else HTMLRaw(raw_mode, raw),
        )
        self.children.append(n)
        return n

    def raw(self, mode, raw):
        n = HTMLNode(self, raw=HTMLRaw(mode, raw))
        self.children.append(n)
        return n

    def comment(self, mode, raw):
        return self.raw(mode, '<!-- ' + raw + ' -->')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    tagc = partialmethod(tag, 'continuation')
    tagl = partialmethod(tag, 'line')
    tagb = partialmethod(tag, 'block')

    rawc = partialmethod(raw, 'continuation')
    rawl = partialmethod(raw, 'line')
    rawb = partialmethod(raw, 'block')

    commentc = partialmethod(comment, 'continuation')
    commentl = partialmethod(comment, 'line')
    commentb = partialmethod(comment, 'block')
