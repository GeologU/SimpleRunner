"""
Basic HTML.
Based on https://www.w3schools.com/tags/ref_byfunc.asp .
"""

from attributes import AttributeHTML
from tags import Tag


class TagDocType(Tag):
    """
    Defines the document type.
    In HTML5 there is only one declaration:
      <!DOCTYPE html>
    The <!DOCTYPE> declaration is NOT case sensitive.
    Based on https://www.w3schools.com/tags/tag_doctype.asp .
    """
    TAG = '!DOCTYPE'
    END_TAG = False
    REQUIRED_ATTRIBUTES = frozenset((AttributeHTML,))


class TagHTML(Tag):
    """
    Defines an HTML document.
    Container for all other HTML elements (except for the <!DOCTYPE> tag).
    Based on https://www.w3schools.com/tags/tag_html.asp .
    """
    TAG = 'html'


class TagHead(Tag):
    """
    Defines information about the document.
    Based on https://www.w3schools.com/tags/tag_head.asp .
    """
    TAG = 'head'
    SUB_TAGS = frozenset(('title', 'style', 'base', 'link', 'meta', 'script', 'noscript'))


class TagTile(Tag):
    """
    Defines a title for the document.
    You can NOT have more than one <title> element in an HTML document.
    Required in an HTML document, if you omit the <title> tag, the document will not validate as HTML.
    Based on https://www.w3schools.com/tags/tag_title.asp .
    """
    TAG = 'title'


class TagBody(Tag):
    """
    Defines the document's body.
    Based on https://www.w3schools.com/tags/tag_body.asp .
    """
    TAG = 'body'


class TagHX(Tag):
    """
    Defines HTML headings.
    The <h1> to <h6> tags are used to define HTML headings.
    <h1> defines the most important heading. <h6> defines the least important heading.
    Based on https://www.w3schools.com/tags/tag_hn.asp .
    """


class TagH1(TagHX):
    TAG = 'h1'


class TagH2(TagHX):
    TAG = 'h2'


class TagH3(TagHX):
    TAG = 'h3'


class TagH4(TagHX):
    TAG = 'h4'


class TagH5(TagHX):
    TAG = 'h5'


class TagH6(TagHX):
    TAG = 'h6'


class TagP(Tag):
    """
    Defines a paragraph
    Based on https://www.w3schools.com/tags/tag_p.asp .
    """
    TAG = 'p'


class TagBr(Tag):
    """
    Inserts a single line break.
    Based on https://www.w3schools.com/tags/tag_br.asp .
    """
    TAG = 'br'
    END_TAG = False


class TagHr(Tag):
    """
    Defines a thematic change in the content.
    Based on https://www.w3schools.com/tags/tag_hr.asp .
    """
    TAG = 'hr'
    END_TAG = False


class TagComment(Tag):
    """
    Defines a comment.
    Based on https://www.w3schools.com/tags/tag_comment.asp .
    """
    TAG = '!--'
    END_TAG = False
