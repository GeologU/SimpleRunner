#!/usr/bin/env python3

import unittest

import with_html_stack


class TestHTMLDocument(unittest.TestCase):

    def setUp(self):
        H = with_html_stack.HTMLDocument()
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
        self.doc = H

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
