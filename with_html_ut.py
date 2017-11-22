#!/usr/bin/env python3

import unittest

import with_html


class TestTextParams(unittest.TestCase):

    def test_indent(self):
        p = with_html.TextParams()
        self.assertEqual(p.indent(), '')

        p = with_html.TextParams(level=2)
        self.assertEqual(p.indent(), '        ')

    def test_inner(self):
        p = with_html.TextParams()
        p2 = p.inner()
        self.assertEqual(p2.level, 1)
        self.assertEqual(p2.level, p.level + 1)
        self.assertEqual(p2.offset, p.offset)
        self.assertEqual(p2.newline, p.newline)

    def test_outer(self):
        p = with_html.TextParams(level=4)
        p2 = p.outer()
        self.assertEqual(p2.level, 3)
        self.assertEqual(p2.level, p.level - 1)
        self.assertEqual(p2.offset, p.offset)
        self.assertEqual(p2.newline, p.newline)

        p3 = p.outer().outer().outer().outer().outer().outer()
        self.assertEqual(p3.level, 0)


class TestHTMLRaw(unittest.TestCase):

    def test_continuation(self):
        p = with_html.TextParams(level=1)
        r = with_html.HTMLRaw('continuation', 'Hi there!')
        self.assertEqual(r.text(p), 'Hi there!')

    def test_line(self):
        p = with_html.TextParams(level=1)
        r = with_html.HTMLRaw('line', 'Hi there!')
        self.assertEqual(r.text(p), p.indent() + 'Hi there!' + p.newline)

    def test_block(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        # raw text without its own intendation

        r1 = with_html.HTMLRaw('block', 'Hi there!')
        self.assertEqual(r1.text(p), '  Hi there!\n')

        r2 = with_html.HTMLRaw('block', 'Hi there!\nHave a great day!\n')
        self.assertEqual(r2.text(p), '  Hi there!\n  Have a great day!\n')

        # raw text with its own intendation

        r3 = with_html.HTMLRaw('block', '\tHi there!\n\tHave a great day!\n or morning!\n')
        self.assertEqual(r3.text(p), '  Hi there!\n  Have a great day!\n or morning!\n')

    def test_wrong_mode(self):
        p = with_html.TextParams()
        r = with_html.HTMLRaw('wrong mode', 'Hi there!')
        with self.assertRaises(RuntimeError):
            r.text(p)


class TestHTMLAttribute(unittest.TestCase):

    def test_text(self):
        a1 = with_html.HTMLAttribute('selected', value=None)
        self.assertEqual(a1.text(), 'selected')

        a2 = with_html.HTMLAttribute('href', 'http://example.com')
        self.assertEqual(a2.text(), 'href="http://example.com"')

        a3 = with_html.HTMLAttribute('xxhttp_equiv', 'Content-type')
        self.assertEqual(a3.text(), 'http-equiv="Content-type"')


class TestHTMLTag(unittest.TestCase):

    def test_attributes(self):
        t = with_html.HTMLTag(
            'line', 'meta',
            xxhttp_equiv='Content-type',
            content='text/html; charset=utf-8',
            xxone_more=None,
        )
        self.assertEqual(
            t.text_attributes(),
            ' http-equiv="Content-type" content="text/html; charset=utf-8" one-more'
        )

    def test_continuation(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        t1 = with_html.HTMLTag('continuation', 'hr')
        self.assertEqual(t1.text(p, raw=None), '<hr />')

        t2 = with_html.HTMLTag('continuation', 'a', href='http://example.com/')
        self.assertEqual(t2.text(p, 'link'), '<a href="http://example.com/">link</a>')

    def test_line(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        t1 = with_html.HTMLTag('line', 'hr')
        self.assertEqual(t1.text(p, raw=None), '  <hr />\n')

        t2 = with_html.HTMLTag('line', 'a', href='http://example.com/')
        self.assertEqual(t2.text(p, 'link'), '  <a href="http://example.com/">link</a>\n')

    def test_block(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        t = with_html.HTMLTag('block', 'a', href='http://example.com/')
        for raw in ['link', '\tlink']:
            r = with_html.HTMLRaw('block', raw)
            self.assertEqual(
                t.text(p, r.text(p.inner())),
                '  <a href="http://example.com/">\n    link\n  </a>\n'
            )

    def test_wrong_mode(self):
        p = with_html.TextParams()
        t = with_html.HTMLTag('wrong mode', 'h1')
        with self.assertRaises(RuntimeError):
            t.text(p, 'Title')


class TestHTMLNode(unittest.TestCase):

    def test_text_children(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')
        n = with_html.HTMLNode()

        self.assertIsNone(n.text_children(p))

        n.tagc('hr')
        n.tagl('br')
        n.tagb('ul')
        self.assertEqual(n.text_children(p), '<hr />  <br />\n  <ul>\n  </ul>\n')

    def test_context(self):
        params = with_html.TextParams(level=1, offset='  ', newline='\n')
        root = with_html.HTMLNode()
        with root.tagb('p') as p:
            p.rawl('Hi there!')
            with p.tagl('a', href='http://example.com/') as a:
                a.rawc('example link')

        # generic check

        self.assertEqual(
            root.text(params),
            '''\
  <p>
    Hi there!
    <a href="http://example.com/">example link</a>
  </p>
''')

        # detailed tree check

        self.assertIsNone(root.node_tag)
        self.assertIsNone(root.node_raw)
        self.assertEqual(len(root.children), 1)

        self.assertIs(p, root.children[0])
        self.assertIsNone(p.node_raw)
        self.assertEqual(p.node_tag.name, 'p')
        self.assertEqual(p.node_tag.mode, 'block')
        self.assertEqual(p.node_tag.attributes, [])
        self.assertEqual(len(p.children), 2)

        self.assertIsNone(p.children[0].node_tag)
        self.assertEqual(len(p.children[0].children), 0)
        self.assertEqual(p.children[0].node_raw.mode, 'line')
        self.assertEqual(p.children[0].node_raw.raw, 'Hi there!')

        self.assertIs(p.children[1], a)
        self.assertEqual(a.node_tag.mode, 'line')
        self.assertEqual(a.node_tag.name, 'a')
        self.assertEqual(len(a.node_tag.attributes), 1)
        self.assertEqual(a.node_tag.attributes[0].attribute, 'href')
        self.assertEqual(a.node_tag.attributes[0].value, 'http://example.com/')
        self.assertIsNone(a.node_raw)
        self.assertEqual(len(a.children), 1)

        self.assertIsNone(a.children[0].node_tag)
        self.assertEqual(len(a.children[0].children), 0)
        self.assertEqual(a.children[0].node_raw.mode, 'continuation')
        self.assertEqual(a.children[0].node_raw.raw, 'example link')

    def test_tag(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        # empty tag

        self.assertEqual(
            with_html.HTMLNode().tagc('hr').text(p),
            '<hr />'
        )

        self.assertEqual(
            with_html.HTMLNode().tagl('hr').text(p),
            '  <hr />\n'
        )

        self.assertEqual(
            with_html.HTMLNode().tagb('hr').text(p),
            '  <hr>\n  </hr>\n'
        )

        # non-empty tag

        self.assertEqual(
            with_html.HTMLNode().tagc('a', 'example link', href="http://example.com/").text(p),
            '<a href="http://example.com/">example link</a>'
        )

        self.assertEqual(
            with_html.HTMLNode().tagl('a', 'example link', href="http://example.com/").text(p),
            '  <a href="http://example.com/">example link</a>\n'
        )

        self.assertEqual(
            with_html.HTMLNode().tagb('a', 'example link', href="http://example.com/").text(p),
            '  <a href="http://example.com/">\n    example link\n  </a>\n'
        )

    def test_raw(self):
        p = with_html.TextParams(level=1, offset='  ', newline='\n')

        self.assertEqual(
            with_html.HTMLNode().rawc('Hello World!').text(p),
            'Hello World!'
        )

        self.assertEqual(
            with_html.HTMLNode().rawl('Hello World!').text(p),
            '  Hello World!\n'
        )

        self.assertEqual(
            with_html.HTMLNode().rawb('Hello World!').text(p),
            '  Hello World!\n'
        )

    def test_comment(self):
        n = with_html.HTMLNode().commentl('just a comment')

        self.assertIsNone(n.node_tag)
        self.assertEqual(len(n.children), 0)
        self.assertIsInstance(n.node_raw, with_html.HTMLRaw)
        self.assertEqual(n.node_raw.mode, 'line')
        self.assertEqual(n.node_raw.raw, '<!-- just a comment -->')

    def make_page(self):
        page = with_html.HTMLNode()
        page.tagl('!DOCTYPE', xxhtml=None)
        page.rawl('')
        html = page.tagb('html')

        with html.tagb('head') as h:
            h.tagl('title', 'Example Domain')
            h.tagl('meta', xxhttp_equiv='Content-type', content='text/html; charset=utf-8')
            with h.tagb('style', xxtype='text/css') as s:
                s.rawl('table, td {border: 1px solid gray; border-collapse: collapse;}')

        html.rawl('')
        with html.tagb('body') as b:
            with b.tagb('table') as t:
                t.tagl('caption', 'Multiplication table')
                for x in range(10):
                    with t.tagl('tr') as l:
                        if x:
                            for y in range(10):
                                if y:
                                    l.tagc('td', str(x * y))
                                else:
                                    l.tagc('td', str(x))
                        else:
                            for item in [''] + [str(a) for a in range(1, 10)]:
                                l.tagc('td', item)
        return page

    def test_debug_page(self):
        page = self.make_page()

        self.maxDiff = None
        self.assertEqual(
            '''\
<!DOCTYPE html>

<html>
    <head>
        <title>Example Domain</title>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
        <style type="text/css">
            table, td {border: 1px solid gray; border-collapse: collapse;}
        </style>
    </head>
    
    <body>
        <table>
            <caption>Multiplication table</caption>
            <tr><td></td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr>
            <tr><td>1</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr>
            <tr><td>2</td><td>2</td><td>4</td><td>6</td><td>8</td><td>10</td><td>12</td><td>14</td><td>16</td><td>18</td></tr>
            <tr><td>3</td><td>3</td><td>6</td><td>9</td><td>12</td><td>15</td><td>18</td><td>21</td><td>24</td><td>27</td></tr>
            <tr><td>4</td><td>4</td><td>8</td><td>12</td><td>16</td><td>20</td><td>24</td><td>28</td><td>32</td><td>36</td></tr>
            <tr><td>5</td><td>5</td><td>10</td><td>15</td><td>20</td><td>25</td><td>30</td><td>35</td><td>40</td><td>45</td></tr>
            <tr><td>6</td><td>6</td><td>12</td><td>18</td><td>24</td><td>30</td><td>36</td><td>42</td><td>48</td><td>54</td></tr>
            <tr><td>7</td><td>7</td><td>14</td><td>21</td><td>28</td><td>35</td><td>42</td><td>49</td><td>56</td><td>63</td></tr>
            <tr><td>8</td><td>8</td><td>16</td><td>24</td><td>32</td><td>40</td><td>48</td><td>56</td><td>64</td><td>72</td></tr>
            <tr><td>9</td><td>9</td><td>18</td><td>27</td><td>36</td><td>45</td><td>54</td><td>63</td><td>72</td><td>81</td></tr>
        </table>
    </body>
</html>\n''',
            page.text(with_html.TextParams(level=0, offset='    ', newline='\n'))
        )

    def test_production_page(self):
        page = self.make_page()

        self.maxDiff = None
        self.assertEqual(
            '<!DOCTYPE html><html><head><title>Example Domain</title><meta http-equiv="Content-type" content="text/html; charset=utf-8" /><style type="text/css">table, td {border: 1px solid gray; border-collapse: collapse;}</style></head><body><table><caption>Multiplication table</caption><tr><td></td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>1</td><td>1</td><td>2</td><td>3</td><td>4</td><td>5</td><td>6</td><td>7</td><td>8</td><td>9</td></tr><tr><td>2</td><td>2</td><td>4</td><td>6</td><td>8</td><td>10</td><td>12</td><td>14</td><td>16</td><td>18</td></tr><tr><td>3</td><td>3</td><td>6</td><td>9</td><td>12</td><td>15</td><td>18</td><td>21</td><td>24</td><td>27</td></tr><tr><td>4</td><td>4</td><td>8</td><td>12</td><td>16</td><td>20</td><td>24</td><td>28</td><td>32</td><td>36</td></tr><tr><td>5</td><td>5</td><td>10</td><td>15</td><td>20</td><td>25</td><td>30</td><td>35</td><td>40</td><td>45</td></tr><tr><td>6</td><td>6</td><td>12</td><td>18</td><td>24</td><td>30</td><td>36</td><td>42</td><td>48</td><td>54</td></tr><tr><td>7</td><td>7</td><td>14</td><td>21</td><td>28</td><td>35</td><td>42</td><td>49</td><td>56</td><td>63</td></tr><tr><td>8</td><td>8</td><td>16</td><td>24</td><td>32</td><td>40</td><td>48</td><td>56</td><td>64</td><td>72</td></tr><tr><td>9</td><td>9</td><td>18</td><td>27</td><td>36</td><td>45</td><td>54</td><td>63</td><td>72</td><td>81</td></tr></table></body></html>',
            page.text(with_html.TextParams(level=0, offset='', newline=''))
        )


if __name__ == '__main__':
    unittest.main()

