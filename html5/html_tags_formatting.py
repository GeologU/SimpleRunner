"""
Basic HTML.
Based on https://www.w3schools.com/tags/ref_byfunc.asp .
"""

from html_attributes import AttributeCite
from html_global_attributes import AttributeDir
from html_tags import Tag


class TagAbbr(Tag):
    """
    Defines an abbreviation or an acronym.
    Based on https://www.w3schools.com/tags/tag_abbr.asp .
    """
    TAG = 'abbr'


class TagAddress(Tag):
    """
    Defines contact information for the author/owner of a document/article.
    Based on https://www.w3schools.com/tags/tag_address.asp .
    """
    TAG = 'address'


class TagB(Tag):
    """
    Defines bold text.
    Based on https://www.w3schools.com/tags/tag_b.asp .
    """
    TAG = 'b'


class TagBdi(Tag):
    """
    Isolates a part of text that might be formatted in a different direction from other text outside it.
    Based on https://www.w3schools.com/tags/tag_bdi.asp .
    """
    TAG = 'bdi'


class TagBdo(Tag):
    """
    Overrides the current text direction.
    Based on https://www.w3schools.com/tags/tag_bdo.asp .
    """
    TAG = 'bdo'
    REQUIRED_ATTRIBUTES = frozenset((AttributeDir,))


class TagBlockQuote(Tag):
    """
    Defines a section that is quoted from another source.
    Based on https://www.w3schools.com/tags/tag_blockquote.asp .
    """
    TAG = 'blockquote'
    REQUIRED_ATTRIBUTES = frozenset((AttributeCite,))


class TagCite(Tag):
    """
    Defines the title of a work.
    Based on https://www.w3schools.com/tags/tag_cite.asp .
    """
    TAG = 'cite'


class TagCode(Tag):
    """
    Defines a piece of computer code.
    Based on https://www.w3schools.com/tags/tag_code.asp .
    """
    TAG = 'code'


class TagDel(Tag):
    """
    Defines text that has been deleted from a document.
    Use <del> and <ins> to markup updates and modifications in a document.
    Browsers will normally strike a line through deleted text and underline inserted text.
    Based on https://www.w3schools.com/tags/tag_del.asp .
    """
    TAG = 'del'


class TagDfn(Tag):
    """
    Represents the defining instance of a term.
    Based on https://www.w3schools.com/tags/tag_dfn.asp .
    """
    TAG = 'dfn'


class TagEm(Tag):
    """
    Defines emphasized text.
    Based on https://www.w3schools.com/tags/tag_em.asp .
    """
    TAG = 'em'


class TagI(Tag):
    """
    Defines a part of text in an alternate voice or mood.
    Based on https://www.w3schools.com/tags/tag_i.asp .
    """
    TAG = 'i'


class TagIns(Tag):
    """
    Defines a text that has been inserted into a document.
    Based on https://www.w3schools.com/tags/tag_ins.asp .
    """
    TAG = 'ins'


class TagKbd(Tag):
    """
    Defines keyboard input.
    Based on https://www.w3schools.com/tags/tag_kbd.asp .
    """
    TAG = 'kbd'


class TagMark(Tag):
    """
    Defines marked/highlighted text.
    Based on https://www.w3schools.com/tags/tag_mark.asp .
    """
    TAG = 'mark'


class TagMeter(Tag):
    """
    Defines a scalar measurement within a known range (a gauge).
    For progress bars, use the <progress> tag.
    Based on https://www.w3schools.com/tags/tag_meter.asp .
    """
    TAG = 'meter'
    REQUIRED_ATTRIBUTES = frozenset((AttributeValue,))


class Tagpre(Tag):
    """
    Defines preformatted text.
    Based on  .
    """
    TAG = 'pre'


class Tagprogress(Tag):
    """
    Represents the progress of a task.
    Based on  .
    """
    TAG = 'progress'


class Tagq(Tag):
    """
    Defines a short quotation.
    Based on  .
    """
    TAG = 'q'


class Tagrp(Tag):
    """
    Defines what to show in browsers that do not support ruby annotations.
    Based on  .
    """
    TAG = 'rp'


class Tagrt(Tag):
    """
    Defines an explanation/pronunciation of characters (for East Asian typography).
    Based on  .
    """
    TAG = 'rt'


class Tagruby(Tag):
    """
    Defines a ruby annotation (for East Asian typography).
    Based on  .
    """
    TAG = 'ruby'


class Tags(Tag):
    """
    Defines text that is no longer correct.
    Based on  .
    """
    TAG = 's'


class Tagsamp(Tag):
    """
    Defines sample output from a computer program.
    Based on  .
    """
    TAG = 'samp'


class Tagsmall(Tag):
    """
    Defines smaller text.
    Based on  .
    """
    TAG = 'small'


class Tagstrong(Tag):
    """
    Defines important text.
    Based on  .
    """
    TAG = 'strong'


class Tagsub(Tag):
    """
    Defines subscripted text.
    Based on  .
    """
    TAG = 'sub'


class Tagsup(Tag):
    """
    Defines superscripted text.
    Based on  .
    """
    TAG = 'sup'


class Tagtemplate(Tag):
    """
    Defines a template.
    Based on  .
    """
    TAG = 'template'


class Tagtime(Tag):
    """
    Defines a date/time.
    Based on  .
    """
    TAG = 'time'


class Tagu(Tag):
    """
    Defines text that should be stylistically different from normal text.
    Based on  .
    """
    TAG = 'u'


class Tagvar(Tag):
    """
    Defines a variable.
    Based on  .
    """
    TAG = 'var'


class Tagwbr(Tag):
    """
    Defines a possible line-break.
    Based on  .
    """
    TAG = 'wbr'
