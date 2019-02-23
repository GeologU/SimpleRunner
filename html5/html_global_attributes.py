#!/usr/bin/env python3

"""
HTML attributes give elements meaning and context.
The global attributes below can be used on any HTML element.
Based on https://www.w3schools.com/tags/ref_standardattributes.asp .
"""

import re

from html_attributes import Attribute


class AttributeAccessKey(Attribute):
    """
    Specifies a shortcut key to activate/focus an element.
    Based on https://www.w3schools.com/tags/att_global_accesskey.asp .
    """
    ATTR = 'accesskey'
    VALID_VALUES = frozenset('abcdefghijklmnopqrstuvwxyz')  # a-z

    def __init__(self, character):
        super().__init__(self.ATTR, character)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeClass(Attribute):
    """
    Specifies one or more classnames for an element (refers to a class in a style sheet).
    Based on https://www.w3schools.com/tags/att_global_class.asp .
    """
    ATTR = 'class'
    CLASSNAME_REGEX = re.compile(r'^[A-Za-z][A-Za-z0-9_-]*( [A-Za-z][A-Za-z0-9_-]*)*$')

    def __init__(self, classname):
        super().__init__(self.ATTR, classname)

    def validate(self):
        super().validate()
        if not self.CLASSNAME_REGEX.match(self.content):
            raise ValueError(super().value_error_message())
        words = self.content.split(' ')
        if len(words) != len(set(words)):
            raise ValueError(super().value_error_message())


class AttributeContentEditable(Attribute):
    """
    Specifies whether the content of an element is editable or not.
    Note: When the contenteditable attribute is not set on an element,
    the element will inherit it from its parent.
    Based on https://www.w3schools.com/tags/att_global_contenteditable.asp .
    """
    ATTR = 'contenteditable'
    VALID_VALUES = frozenset(('true', 'false',))

    def __init__(self, flag):
        if isinstance(flag, bool):
            flag = 'true' if flag else 'false'
        super().__init__(self.ATTR, flag)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeDataStar(Attribute):
    """
    Used to store custom data private to the page or application.
    Based on https://www.w3schools.com/tags/att_global_data.asp .
    """
    ATTR = 'data-*'
    STAR_REGEX = re.compile(r'^data[-][a-z-]*[a-z]$')

    def __init__(self, name, somevalue):
        if isinstance(name, str) and not name.startswith('data-'):
            name = 'data-' + name
        super().__init__(name, somevalue)

    def validate(self):
        super().validate()

        name_error_message = 'Bad name for attribute {}: {}'.format(self.ATTR, repr(self.name))
        if not isinstance(self.name, str):
            raise ValueError(name_error_message)
        if not self.STAR_REGEX.match(self.name):
            raise ValueError(name_error_message)


class AttributeDir(Attribute):
    """
    Specifies the text direction for the content in an element.
    Based on https://www.w3schools.com/tags/att_global_dir.asp .
    """
    ATTR = 'dir'
    VALID_VALUES = {'ltr', 'rtl', 'auto'}

    def __init__(self, direction):
        if direction is None:
            direction = 'auto'
        super().__init__(self.ATTR, direction)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeDraggable(Attribute):
    """
    Specifies whether an element is draggable or not.
    Based on https://www.w3schools.com/tags/att_global_draggable.asp .
    """
    ATTR = 'draggable'
    VALID_VALUES = {'true', 'false', 'auto'}

    def __init__(self, flag):
        if flag is None:
            flag = 'auto'
        if isinstance(flag, bool):
            flag = 'true' if flag else 'false'
        super().__init__(self.ATTR, flag)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeDropZone(Attribute):
    """
    Specifies whether the dragged data is copied, moved, or linked, when dropped.
    Based on https://www.w3schools.com/tags/att_global_dropzone.asp .
    """
    ATTR = 'dropzone'
    VALID_VALUES = {'copy', 'move', 'link'}

    def __init__(self, flag):
        super().__init__(self.ATTR, flag)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeHidden(Attribute):
    """
    Specifies that an element is not yet, or is no longer, relevant.
    Based on https://www.w3schools.com/tags/att_global_hidden.asp .
    """
    ATTR = 'hidden'

    def __init__(self):
        super().__init__(self.ATTR, '')

    def __str__(self):
        return ' hidden'


class AttributeID(Attribute):
    """
    Specifies a unique id for an element.
    Based on https://www.w3schools.com/tags/att_global_id.asp .
    """
    ATTR = 'id'
    SPACE_RE = re.compile(r'\s+')

    def __init__(self, id_str):
        super().__init__(self.ATTR, id_str)

    def validate(self):
        super().validate()
        if len(self.content) < 1:
            raise ValueError(super().value_error_message())
        if self.SPACE_RE.search(self.content):
            raise ValueError(super().value_error_message())


class AttributeLang(Attribute):
    """
    Specifies the language of the element's content
    Based on https://www.w3schools.com/tags/att_global_lang.asp
         and https://www.w3schools.com/tags/ref_language_codes.asp .
    """
    ATTR = 'lang'
    ISO_LANGUAGE_CODES = frozenset([
        'ab', 'aa', 'af', 'ak', 'sq', 'am', 'ar', 'an', 'hy', 'as', 'av', 'ae',
        'ay', 'az', 'bm', 'ba', 'eu', 'be', 'bn', 'bh', 'bi', 'bs', 'br', 'bg',
        'my', 'ca', 'ch', 'ce', 'ny', 'zh', 'zh-Hans', 'zh-Hant', 'cv', 'kw',
        'co', 'cr', 'hr', 'cs', 'da', 'dv', 'nl', 'dz', 'en', 'eo', 'et', 'ee',
        'fo', 'fj', 'fi', 'fr', 'ff', 'gl', 'gd', 'gv', 'ka', 'de', 'el', 'kl',
        'gn', 'gu', 'ht', 'ha', 'he', 'hz', 'hi', 'ho', 'hu', 'is', 'io', 'ig',
        'id', 'in', 'ia', 'ie', 'iu', 'ik', 'ga', 'it', 'ja', 'jv', 'kl', 'kn',
        'kr', 'ks', 'kk', 'km', 'ki', 'rw', 'rn', 'ky', 'kv', 'kg', 'ko', 'ku',
        'kj', 'lo', 'la', 'lv', 'li', 'ln', 'lt', 'lu', 'lg', 'lb', 'gv', 'mk',
        'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mh', 'mo', 'mn', 'na', 'nv', 'ng',
        'nd', 'ne', 'no', 'nb', 'nn', 'ii', 'oc', 'oj', 'cu', 'or', 'om', 'os',
        'pi', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'rm', 'ro', 'ru', 'se', 'sm',
        'sg', 'sa', 'sr', 'sh', 'st', 'tn', 'sn', 'ii', 'sd', 'si', 'ss', 'sk',
        'sl', 'so', 'nr', 'es', 'su', 'sw', 'ss', 'sv', 'tl', 'ty', 'tg', 'ta',
        'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tr', 'tk', 'tw', 'ug', 'uk',
        'ur', 'uz', 've', 'vi', 'vo', 'wa', 'cy', 'wo', 'fy', 'xh', 'yi', 'ji',
        'yo', 'za', 'zu',
    ])

    def __init__(self, language_code):
        super().__init__(self.ATTR, language_code)

    def validate(self):
        super().validate()
        if self.content not in self.ISO_LANGUAGE_CODES:
            raise ValueError(super().value_error_message())


class AttributeSpellCheck(Attribute):
    """
    Specifies whether the element is to have its spelling and grammar checked or not.
    Based on https://www.w3schools.com/tags/att_global_spellcheck.asp .
    """
    ATTR = 'spellcheck'
    VALID_VALUES = {'true', 'false'}

    def __init__(self, flag):
        if isinstance(flag, bool):
            flag = 'true' if flag else 'false'
        super().__init__(self.ATTR, flag)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


class AttributeStyle(Attribute):
    """
    Specifies an inline CSS style for an element.
    Based on https://www.w3schools.com/tags/att_global_style.asp .
    """
    ATTR = 'style'

    def __init__(self, style_definitions):
        super().__init__(self.ATTR, style_definitions)


class AttributeTabIndex(Attribute):
    """
    Specifies the tabbing order of an element.
    Based on https://www.w3schools.com/tags/att_global_tabindex.asp .
    """
    ATTR = 'tabindex'

    def __init__(self, number):
        if isinstance(number, int):
            number = str(number)
        super().__init__(self.ATTR, number)

    def validate(self):
        super().validate()
        if not self.content.isdigit():
            raise ValueError(super().value_error_message())
        if int(self.content) < 1:
            raise ValueError(super().value_error_message())


class AttributeTitle(Attribute):
    """
    Specifies extra information about an element.
    Based on https://www.w3schools.com/tags/att_global_title.asp .
    """
    ATTR = 'title'

    def __init__(self, text):
        super().__init__(self.ATTR, text)


class AttributeTranslate(Attribute):
    """
    Specifies whether the content of an element should be translated or not.
    Based on https://www.w3schools.com/tags/att_global_translate.asp .
    """
    ATTR = 'translate'
    VALID_VALUES = {'yes', 'no'}

    def __init__(self, flag):
        if isinstance(flag, bool):
            flag = 'yes' if flag else 'no'
        super().__init__(self.ATTR, flag)

    def validate(self):
        super().validate()
        if self.content not in self.VALID_VALUES:
            raise ValueError(super().value_error_message())


GLOBAL_ATTRIBUTES = [
    AttributeAccessKey,
    AttributeClass,
    AttributeContentEditable,
    AttributeDataStar,
    AttributeDir,
    AttributeDraggable,
    AttributeDropZone,
    AttributeHidden,
    AttributeID,
    AttributeLang,
    AttributeSpellCheck,
    AttributeStyle,
    AttributeTabIndex,
    AttributeTitle,
    AttributeTranslate,
]
GLOBAL_ATTRIBUTE_BY_NAME = {x.ATTR: x for x in GLOBAL_ATTRIBUTES}


def global_attribute(name, text=None):
    if name.startswith('data-'):
        return AttributeDataStar(name, text)
    elif name == 'hidden':
        if text is not None:
            raise ValueError('Got value where None is expected: ' + repr(text))
        return AttributeHidden()
    elif name in GLOBAL_ATTRIBUTE_BY_NAME:
        return GLOBAL_ATTRIBUTE_BY_NAME[name](text)
    return None
