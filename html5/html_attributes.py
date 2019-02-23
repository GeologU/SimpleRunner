#!/usr/bin/env python3

"""
Attributes provide additional information about HTML elements.
Based on https://www.w3schools.com/html/html_attributes.asp .
"""


def quote(text):
    if '"' not in text:
        q, t = '"', text
    elif "'" not in text:
        q, t = "'", text
    else:
        q = '"'
        t = text.replace('"', '\\"')
    return q + t + q


class Attribute:

    def __init__(self, name, content):
        self.name = name
        self.content = content
        self.validate()
        self.quoted = quote(content)

    def value_error_message(self):
        return 'Bad value for attribute {}: {}'.format(self.name, repr(self.content))

    def validate(self):
        if not isinstance(self.content, str):
            raise ValueError(self.value_error_message())

    def __str__(self):
        return ' {}={}'.format(self.name, self.quoted)


class AttributeHTML(Attribute):
    ATTR = 'html'

    def __init__(self):
        super().__init__(self.ATTR, '')

    def __str__(self):
        return ' html'


class AttributeCite(Attribute):
    """
    Specifies a URL to a document
     - that explains the reason why the text was deleted;
     - the source of the quotation.
    Based on https://www.w3schools.com/tags/att_blockquote_cite.asp .
    Based on https://www.w3schools.com/tags/att_del_cite.asp .
    """
    ATTR = 'cite'

    def __init__(self, url: str):
        super().__init__(self.ATTR, url)


class AttributeDateTime(Attribute):
    """
    The datetime attribute specifies the date and time when the text was deleted.
    Based on https://www.w3schools.com/tags/att_del_datetime.asp .
    """
    ATTR = 'datetime'

    def __init__(self, datetime: str):
        super().__init__(self.ATTR, datetime)

    def validate(self):
        super().validate()
        raise NotImplementedError
