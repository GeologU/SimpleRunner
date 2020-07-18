#!/usr/bin/env python3

import unittest

import with_html_stack


class TestHTMLDocument(unittest.TestCase):

    def setUp(self):
        doc = with_html_stack.HTMLDocument()
        doc('!doctype', html=None)
        with doc('html', lang='en'):
            with doc('head'):
                doc('title', raw='Example Domain')
                doc('meta', charset='utf-8')
            with doc('body'):
                with doc('div'):
                    doc('h1', raw='Example Domain')
                    with doc('p'):
                        doc.raw('This domain is for use in illustrative examples in documents. You ')
                        doc.raw('may use this domain in literature without prior coordination or asking for permission.')
                    with doc('p'):
                        with doc('a', href='https://www.iana.org/domains/example'):
                            doc.raw('More information')
        self.doc = doc

    def test_dev(self):
        self.assertEqual(self.doc.text(with_html_stack.DEV_PARAMS), '''\
<!doctype html>
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
''')

    def test_prod(self):
        self.assertEqual(self.doc.text(with_html_stack.PROD_PARAMS), '''\
<!doctype html><html lang="en"><head><title>Example Domain</title><meta charset="utf-8"/></head><body><div><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p><p><a href="https://www.iana.org/domains/example">More information</a></p></div></body></html>''')

    def test_append(self):
        head = with_html_stack.HTMLDocument()
        with head('head'):
            head('title', raw='Example Domain')
            head('meta', charset='utf-8')

        content = with_html_stack.HTMLDocument()
        content('h1', raw='Example Domain')
        with content('p'):
            content.raw('This domain is for use in illustrative examples in documents. You ')
            content.raw('may use this domain in literature without prior coordination or asking for permission.')

        doc = with_html_stack.HTMLDocument()
        doc('!doctype', html=None)
        with doc('html', lang='en'):
            doc.append(head)
            with doc('body'):
                with doc('div'):
                    doc.append(content)
                    with doc('p'):
                        with doc('a', href='https://www.iana.org/domains/example'):
                            doc.raw('More information')

        self.assertEqual(doc.text(with_html_stack.DEV_PARAMS), '''\
<!doctype html>
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
''')
