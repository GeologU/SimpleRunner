#!/usr/bin/env python3

"""Tag-specific attributes."""

from attributes import Attribute


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

form 	form_id 	Specifies one or more forms the <meter> element belongs to
high 	number 	Specifies the range that is considered to be a high value
low 	number 	Specifies the range that is considered to be a low value
max 	number 	Specifies the maximum value of the range
min 	number 	Specifies the minimum value of the range
optimum 	number 	Specifies what value is the optimal value for the gauge
value 	number 	Required. Specifies the current value of the gauge
