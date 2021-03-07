#!/usr/bin/env python3

import unittest

import with_html_stack


class TestFunctions(unittest.TestCase):

    def test_to_safe_name(self):
        self.assertEqual(with_html_stack.to_safe_name(name='testname'), 'testname')
        self.assertEqual(with_html_stack.to_safe_name(name='testname', safe_prefix='xx_'), 'testname')

        self.assertEqual(with_html_stack.to_safe_name(name='test-name'), '_test_name')
        self.assertEqual(with_html_stack.to_safe_name(name='test-name', safe_prefix='xx_'), 'xx_test_name')
        self.assertEqual(with_html_stack.to_safe_name(name='test-name-2'), '_test_name_2')

        self.assertEqual(with_html_stack.to_safe_name(name='id'), '_id')
        self.assertEqual(with_html_stack.to_safe_name(name='id', safe_prefix='xx_'), 'xx_id')

    def test_from_safe_name(self):
        self.assertEqual(with_html_stack.from_safe_name(name='testname'), 'testname')
        self.assertEqual(with_html_stack.from_safe_name(name='testname', safe_prefix='xx_'), 'testname')

        self.assertEqual(with_html_stack.from_safe_name(name='_test_name'), 'test-name')
        self.assertEqual(with_html_stack.from_safe_name(name='xx_test_name', safe_prefix='xx_'), 'test-name')
        self.assertEqual(with_html_stack.from_safe_name(name='_test_name_2'), 'test-name-2')

        self.assertEqual(with_html_stack.from_safe_name(name='_id'), 'id')
        self.assertEqual(with_html_stack.from_safe_name(name='xx_id', safe_prefix='xx_'), 'id')

    def test_html_as_code(self):
        self.assertEqual(with_html_stack.html_as_code('A&B'), "'A&B'")
        self.assertEqual(with_html_stack.html_as_code('A&amp;B'), "html.escape('A&B')")
        self.assertEqual(with_html_stack.html_as_code(None), 'None')

    def test_get_indent(self):
        self.assertEqual(with_html_stack.get_indent(''), '')
        self.assertEqual(with_html_stack.get_indent(' '), ' ')
        self.assertEqual(with_html_stack.get_indent(' \t\r text'), ' \t\r ')
        self.assertEqual(with_html_stack.get_indent('text \t\r text'), '')


class TestTextParams(unittest.TestCase):

    def test_str(self):
        self.assertEqual(
            str(with_html_stack.DEV_PARAMS),
            "TextParams(level=0, offset='    ', newline='\\n')"
        )
        self.assertEqual(
            str(with_html_stack.DEV_PARAMS.inner),
            "TextParams(level=1, offset='    ', newline='\\n')"
        )

        self.assertEqual(
            str(with_html_stack.PROD_PARAMS),
            "TextParams(level=0, offset='', newline='')"
        )
        self.assertEqual(
            str(with_html_stack.PROD_PARAMS.inner),
            "TextParams(level=1, offset='', newline='')"
        )

    def test_indent(self):
        p = with_html_stack.TextParams()
        self.assertEqual(p.indent, '')

        p = with_html_stack.TextParams(level=2)
        self.assertEqual(p.indent, '        ')

    def test_inner(self):
        p = with_html_stack.TextParams()
        p2 = p.inner
        self.assertEqual(p2.level, 1)
        self.assertEqual(p2.level, p.level + 1)
        self.assertEqual(p2.offset, p.offset)
        self.assertEqual(p2.newline, p.newline)

    def test_line(self):
        p = with_html_stack.TextParams()
        self.assertEqual(p.line(middle='some middle text'), 'some middle text\n')
        self.assertEqual(p.line(middle='some middle text', indent='\t'), '\tsome middle text\n')

        p2 = with_html_stack.TextParams(level=1, newline='\r\n')
        self.assertEqual(p2.line(middle='some middle text'), '    some middle text\r\n')
        self.assertEqual(p2.line(middle='some middle text', indent='\t'), '\tsome middle text\r\n')

    def test_text_dev_params(self):
        p = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(p.text([
                '\rfirst line',
                '\tsecond line',
                ' third line',
            ]), '''\
    \rfirst line
    \tsecond line
     third line
''')

        p = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(p.text([
                '\tfirst line',
                '\t\tsecond line',
                '\tthird line',
            ], '-p-', '-s-'), '''\
    -p-first line-s-
    \t-p-second line-s-
    -p-third line-s-
''')

        p = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(p.text([]), '')

        p = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(p.text(['one line']), '    one line\n')

    def test_text_prod_params(self):
        p = with_html_stack.PROD_PARAMS.inner
        self.assertEqual(p.text([
                '\tfirst line',
                '\t\tsecond line',
                '\tthird line',
            ], '-p-', '-s-'),
            '-p-first line-s-\t-p-second line-s--p-third line-s-'
        )

    def test_none_fix(self):
        p = with_html_stack.PROD_PARAMS.inner
        self.assertEqual(p.text([
                '\tfirst line',
                '\t\tsecond line',
                '\tthird line',
            ], None, None),
            'first line\tsecond linethird line'
        )


class TestHTMLRaw(unittest.TestCase):

    def test_text(self):
        raw = with_html_stack.HTMLRaw('some raw text', prefix='-p-', suffix='-s-')
        self.assertEqual(
            raw.text(with_html_stack.DEV_PARAMS.inner),
            '    -p-some raw text-s-\n'
        )
        self.assertEqual(
            raw.text(with_html_stack.PROD_PARAMS),
            '-p-some raw text-s-'
        )

        raw = with_html_stack.HTMLRaw('some multiline\nraw text\n', prefix='-p-', suffix='-s-')
        self.assertEqual(
            raw.text(with_html_stack.DEV_PARAMS.inner),
            '    -p-some multiline-s-\n    -p-raw text-s-\n'
        )
        self.assertEqual(
            raw.text(with_html_stack.PROD_PARAMS),
            '-p-some multiline-s--p-raw text-s-'
        )


    def test_code(self):
        raw = with_html_stack.HTMLRaw('some raw text')
        self.assertEqual(
            raw.code(with_html_stack.DEV_PARAMS.inner),
            "    doc.raw('some raw text')\n"
        )

        raw = with_html_stack.HTMLRaw('some raw text', prefix='-p-', suffix='-s-')
        self.assertEqual(
            raw.code(with_html_stack.DEV_PARAMS.inner),
            "    doc.raw('some raw text', prefix='-p-', suffix='-s-')\n"
        )
        self.assertEqual(
            raw.code(with_html_stack.PROD_PARAMS),
            "doc.raw('some raw text', prefix='-p-', suffix='-s-')"
        )

        raw = with_html_stack.HTMLRaw('some multiline\nraw text\n', prefix='-p-', suffix='-s-')
        self.assertEqual(
            raw.code(with_html_stack.DEV_PARAMS.inner),
            "    doc.raw('some multiline\\nraw text\\n', prefix='-p-', suffix='-s-')\n"
        )
        self.assertEqual(
            raw.code(with_html_stack.PROD_PARAMS),
            "doc.raw('some multiline\\nraw text\\n', prefix='-p-', suffix='-s-')"
        )


class TestHTMLComment(unittest.TestCase):

    def test_text(self):
        raw = with_html_stack.HTMLComment('some raw text')
        self.assertEqual(
            raw.text(with_html_stack.DEV_PARAMS.inner),
            '    <!-- some raw text -->\n'
        )
        self.assertEqual(
            raw.text(with_html_stack.PROD_PARAMS),
            '<!-- some raw text -->'
        )

        raw = with_html_stack.HTMLComment('some multiline\nraw text\n')
        self.assertEqual(
            raw.text(with_html_stack.DEV_PARAMS.inner),
            '    <!-- some multiline -->\n    <!-- raw text -->\n'
        )
        self.assertEqual(
            raw.text(with_html_stack.PROD_PARAMS),
            '<!-- some multiline --><!-- raw text -->'
        )


    def test_code(self):
        raw = with_html_stack.HTMLComment('some raw text')
        self.assertEqual(
            raw.code(with_html_stack.DEV_PARAMS.inner),
            "    doc.comment('some raw text')\n"
        )
        self.assertEqual(
            raw.code(with_html_stack.PROD_PARAMS),
            "doc.comment('some raw text')"
        )

        raw = with_html_stack.HTMLComment('some multiline\nraw text\n')
        self.assertEqual(
            raw.code(with_html_stack.DEV_PARAMS.inner),
            "    doc.comment('some multiline\\nraw text\\n')\n"
        )
        self.assertEqual(
            raw.code(with_html_stack.PROD_PARAMS),
            "doc.comment('some multiline\\nraw text\\n')"
        )


class TestHTMLAttribute(unittest.TestCase):

    def test_test(self):
        # check default values
        self.assertEqual(with_html_stack.HTMLAttribute('attr').text(), 'attr')
        self.assertEqual(with_html_stack.HTMLAttribute('attr', '<value>').text(), 'attr="<value>"')

        # check various cases
        # input data produced with:
        # >>> list(itertools.product(('attr', '_complex_name'), ('value', '<value>', None), (True, False), ('',)))
        for attr, value, escape, expected in [
            ('attr', 'value', True, 'attr="value"'),
            ('attr', 'value', False, 'attr="value"'),
            ('attr', '<value>', True, 'attr="&lt;value&gt;"'),
            ('attr', '<value>', False, 'attr="<value>"'),
            ('attr', None, True, 'attr'),
            ('attr', None, False, 'attr'),
            ('_complex_name', 'value', True, 'complex-name="value"'),
            ('_complex_name', 'value', False, 'complex-name="value"'),
            ('_complex_name', '<value>', True, 'complex-name="&lt;value&gt;"'),
            ('_complex_name', '<value>', False, 'complex-name="<value>"'),
            ('_complex_name', None, True, 'complex-name'),
            ('_complex_name', None, False, 'complex-name')
        ]:
            with self.subTest(attr=attr, value=value, escape=escape, expected=expected):
                self.assertEqual(
                    with_html_stack.HTMLAttribute(attribute=attr, value=value, escape=escape).text(),
                    expected
                )

    def test_code(self):
        # check default values
        self.assertEqual(with_html_stack.HTMLAttribute('attr').code(), 'attr=None')
        self.assertEqual(with_html_stack.HTMLAttribute('attr', '<value>').code(), "attr='<value>'")

        # check various cases
        # input data produced with:
        # >>> list(itertools.product(('attr', '_complex_name'), ('value', '<value>', None), (True, False), ('',)))
        for attr, value, escape, expected in [
            ('attr', 'value', True, "attr='value'"),
            ('attr', 'value', False, "attr='value'"),
            ('attr', '<value>', True, "attr=html.escape('<value>')"),
            ('attr', '<value>', False, "attr='<value>'"),
            ('attr', None, True, 'attr=None'),
            ('attr', None, False, 'attr=None'),
            ('_complex_name', 'value', True, "_complex_name='value'"),
            ('_complex_name', 'value', False, "_complex_name='value'"),
            ('_complex_name', '<value>', True, "_complex_name=html.escape('<value>')"),
            ('_complex_name', '<value>', False, "_complex_name='<value>'"),
            ('_complex_name', None, True, '_complex_name=None'),
            ('_complex_name', None, False, '_complex_name=None')
        ]:
            with self.subTest(attr=attr, value=value, escape=escape, expected=expected):
                self.assertEqual(
                    with_html_stack.HTMLAttribute(attribute=attr, value=value, escape=escape).code(),
                    expected
                )


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
