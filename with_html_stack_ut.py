#!/usr/bin/env python3

import unittest

import with_html_stack


class TestFunctions(unittest.TestCase):
    def test_to_safe_name(self):
        self.assertEqual(with_html_stack.to_safe_name(name="testname"), "testname")
        self.assertEqual(with_html_stack.to_safe_name(name="testname", safe_prefix="xx_"), "testname")

        self.assertEqual(with_html_stack.to_safe_name(name="test-name"), "_test_name")
        self.assertEqual(with_html_stack.to_safe_name(name="test-name", safe_prefix="xx_"), "xx_test_name")
        self.assertEqual(with_html_stack.to_safe_name(name="test-name-2"), "_test_name_2")

        self.assertEqual(with_html_stack.to_safe_name(name="id"), "_id")
        self.assertEqual(with_html_stack.to_safe_name(name="id", safe_prefix="xx_"), "xx_id")

    def test_from_safe_name(self):
        self.assertEqual(with_html_stack.from_safe_name(name="testname"), "testname")
        self.assertEqual(with_html_stack.from_safe_name(name="testname", safe_prefix="xx_"), "testname")

        self.assertEqual(with_html_stack.from_safe_name(name="_test_name"), "test-name")
        self.assertEqual(with_html_stack.from_safe_name(name="xx_test_name", safe_prefix="xx_"), "test-name")
        self.assertEqual(with_html_stack.from_safe_name(name="_test_name_2"), "test-name-2")

        self.assertEqual(with_html_stack.from_safe_name(name="_id"), "id")
        self.assertEqual(with_html_stack.from_safe_name(name="xx_id", safe_prefix="xx_"), "id")

    def test_html_as_code(self):
        self.assertEqual(with_html_stack.html_as_code("A&B"), "'A&B'")
        self.assertEqual(with_html_stack.html_as_code("A&amp;B"), "html.escape('A&B')")
        self.assertEqual(with_html_stack.html_as_code(None), "None")

    def test_get_indent(self):
        self.assertEqual(with_html_stack.get_indent(""), "")
        self.assertEqual(with_html_stack.get_indent(" "), " ")
        self.assertEqual(with_html_stack.get_indent(" \t\r text"), " \t\r ")
        self.assertEqual(with_html_stack.get_indent("text \t\r text"), "")


class TestTextParams(unittest.TestCase):
    def test_str(self):
        self.assertEqual(str(with_html_stack.DEV_PARAMS), "TextParams(level=0, offset='    ', newline='\\n')")
        self.assertEqual(str(with_html_stack.DEV_PARAMS.inner), "TextParams(level=1, offset='    ', newline='\\n')")

        self.assertEqual(str(with_html_stack.PROD_PARAMS), "TextParams(level=0, offset='', newline='')")
        self.assertEqual(str(with_html_stack.PROD_PARAMS.inner), "TextParams(level=1, offset='', newline='')")

    def test_indent(self):
        params = with_html_stack.TextParams()
        self.assertEqual(params.indent, "")

        params2 = with_html_stack.TextParams(level=2)
        self.assertEqual(params2.indent, "        ")

    def test_inner(self):
        params = with_html_stack.TextParams()
        params2 = params.inner
        self.assertEqual(params2.level, 1)
        self.assertEqual(params2.level, params.level + 1)
        self.assertEqual(params2.offset, params.offset)
        self.assertEqual(params2.newline, params.newline)

    def test_line(self):
        params = with_html_stack.TextParams()
        self.assertEqual(params.line(middle="some middle text"), "some middle text\n")
        self.assertEqual(params.line(middle="some middle text", indent="\t"), "\tsome middle text\n")

        params2 = with_html_stack.TextParams(level=1, newline="\r\n")
        self.assertEqual(params2.line(middle="some middle text"), "    some middle text\r\n")
        self.assertEqual(params2.line(middle="some middle text", indent="\t"), "\tsome middle text\r\n")

    def test_text_dev_params(self):
        params = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(
            params.text(
                [
                    "\rfirst line",
                    "\tsecond line",
                    " third line",
                ]
            ),
            """\
    \rfirst line
    \tsecond line
     third line
""",
        )

        params = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(
            params.text(
                [
                    "\tfirst line",
                    "\t\tsecond line",
                    "\tthird line",
                ],
                "-p-",
                "-s-",
            ),
            """\
    -p-first line-s-
    \t-p-second line-s-
    -p-third line-s-
""",
        )

        params = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(params.text([]), "")

        params = with_html_stack.DEV_PARAMS.inner
        self.assertEqual(params.text(["one line"]), "    one line\n")

    def test_text_prod_params(self):
        params = with_html_stack.PROD_PARAMS.inner
        self.assertEqual(
            params.text(
                [
                    "\tfirst line",
                    "\t\tsecond line",
                    "\tthird line",
                ],
                "-p-",
                "-s-",
            ),
            "-p-first line-s-\t-p-second line-s--p-third line-s-",
        )

    def test_none_fix(self):
        params = with_html_stack.PROD_PARAMS.inner
        self.assertEqual(
            params.text(
                [
                    "\tfirst line",
                    "\t\tsecond line",
                    "\tthird line",
                ],
                None,
                None,
            ),
            "first line\tsecond linethird line",
        )


class TestHTMLRaw(unittest.TestCase):
    def test_text(self):
        raw = with_html_stack.HTMLRaw("some raw text", prefix="-p-", suffix="-s-")
        self.assertEqual(raw.as_text(with_html_stack.DEV_PARAMS.inner), "    -p-some raw text-s-\n")
        self.assertEqual(raw.as_text(with_html_stack.PROD_PARAMS), "-p-some raw text-s-")

        raw = with_html_stack.HTMLRaw("some multiline\nraw text\n", prefix="-p-", suffix="-s-")
        self.assertEqual(
            raw.as_text(with_html_stack.DEV_PARAMS.inner), "    -p-some multiline-s-\n    -p-raw text-s-\n"
        )
        self.assertEqual(raw.as_text(with_html_stack.PROD_PARAMS), "-p-some multiline-s--p-raw text-s-")

    def test_code(self):
        raw = with_html_stack.HTMLRaw("some raw text")
        self.assertEqual(raw.as_code(with_html_stack.DEV_PARAMS.inner), "    doc.raw('some raw text')\n")

        raw = with_html_stack.HTMLRaw("some raw text", prefix="-p-", suffix="-s-")
        self.assertEqual(
            raw.as_code(with_html_stack.DEV_PARAMS.inner), "    doc.raw('some raw text', prefix='-p-', suffix='-s-')\n"
        )
        self.assertEqual(
            raw.as_code(with_html_stack.PROD_PARAMS), "doc.raw('some raw text', prefix='-p-', suffix='-s-')"
        )

        raw = with_html_stack.HTMLRaw("some multiline\nraw text\n", prefix="-p-", suffix="-s-")
        self.assertEqual(
            raw.as_code(with_html_stack.DEV_PARAMS.inner),
            "    doc.raw('some multiline\\nraw text\\n', prefix='-p-', suffix='-s-')\n",
        )
        self.assertEqual(
            raw.as_code(with_html_stack.PROD_PARAMS),
            "doc.raw('some multiline\\nraw text\\n', prefix='-p-', suffix='-s-')",
        )


class TestHTMLComment(unittest.TestCase):
    def test_text(self):
        raw = with_html_stack.HTMLComment("some raw text")
        self.assertEqual(raw.as_text(with_html_stack.DEV_PARAMS.inner), "    <!-- some raw text -->\n")
        self.assertEqual(raw.as_text(with_html_stack.PROD_PARAMS), "<!-- some raw text -->")

        raw = with_html_stack.HTMLComment("some multiline\nraw text\n")
        self.assertEqual(
            raw.as_text(with_html_stack.DEV_PARAMS.inner), "    <!-- some multiline -->\n    <!-- raw text -->\n"
        )
        self.assertEqual(raw.as_text(with_html_stack.PROD_PARAMS), "<!-- some multiline --><!-- raw text -->")

    def test_code(self):
        raw = with_html_stack.HTMLComment("some raw text")
        self.assertEqual(raw.as_code(with_html_stack.DEV_PARAMS.inner), "    doc.comment('some raw text')\n")
        self.assertEqual(raw.as_code(with_html_stack.PROD_PARAMS), "doc.comment('some raw text')")

        raw = with_html_stack.HTMLComment("some multiline\nraw text\n")
        self.assertEqual(
            raw.as_code(with_html_stack.DEV_PARAMS.inner), "    doc.comment('some multiline\\nraw text\\n')\n"
        )
        self.assertEqual(raw.as_code(with_html_stack.PROD_PARAMS), "doc.comment('some multiline\\nraw text\\n')")


class TestHTMLAttribute(unittest.TestCase):
    def test_test(self):
        # check default values
        self.assertEqual(with_html_stack.HTMLAttribute("attr").as_text(), "attr")
        self.assertEqual(with_html_stack.HTMLAttribute("attr", "<value>").as_text(), 'attr="<value>"')

        # check various cases
        # input data produced with:
        # >>> list(itertools.product(('attr', '_complex_name'), ('value', '<value>', None), (True, False), ('',)))
        for attr, value, escape, expected in [
            ("attr", "value", True, 'attr="value"'),
            ("attr", "value", False, 'attr="value"'),
            ("attr", "<value>", True, 'attr="&lt;value&gt;"'),
            ("attr", "<value>", False, 'attr="<value>"'),
            ("attr", None, True, "attr"),
            ("attr", None, False, "attr"),
            ("_complex_name", "value", True, 'complex-name="value"'),
            ("_complex_name", "value", False, 'complex-name="value"'),
            ("_complex_name", "<value>", True, 'complex-name="&lt;value&gt;"'),
            ("_complex_name", "<value>", False, 'complex-name="<value>"'),
            ("_complex_name", None, True, "complex-name"),
            ("_complex_name", None, False, "complex-name"),
        ]:
            with self.subTest(attr=attr, value=value, escape=escape, expected=expected):
                self.assertEqual(
                    with_html_stack.HTMLAttribute(attribute=attr, value=value, escape=escape).as_text(), expected
                )

    def test_code(self):
        # check default values
        self.assertEqual(with_html_stack.HTMLAttribute("attr").as_code(), "attr=None")
        self.assertEqual(with_html_stack.HTMLAttribute("attr", "<value>").as_code(), "attr='<value>'")

        # check various cases
        # input data produced with:
        # >>> list(itertools.product(('attr', '_complex_name'), ('value', '<value>', None), (True, False), ('',)))
        for attr, value, escape, expected in [
            ("attr", "value", True, "attr='value'"),
            ("attr", "value", False, "attr='value'"),
            ("attr", "<value>", True, "attr=html.escape('<value>')"),
            ("attr", "<value>", False, "attr='<value>'"),
            ("attr", None, True, "attr=None"),
            ("attr", None, False, "attr=None"),
            ("_complex_name", "value", True, "_complex_name='value'"),
            ("_complex_name", "value", False, "_complex_name='value'"),
            ("_complex_name", "<value>", True, "_complex_name=html.escape('<value>')"),
            ("_complex_name", "<value>", False, "_complex_name='<value>'"),
            ("_complex_name", None, True, "_complex_name=None"),
            ("_complex_name", None, False, "_complex_name=None"),
        ]:
            with self.subTest(attr=attr, value=value, escape=escape, expected=expected):
                self.assertEqual(
                    with_html_stack.HTMLAttribute(attribute=attr, value=value, escape=escape).as_code(), expected
                )


class TestHTMLTag(unittest.TestCase):
    def test_text_attributes(self):
        self.assertEqual(
            with_html_stack.HTMLTag("a", href="http://&&.ru", _id="ID", non=None).text_attributes(),
            ' href="http://&&.ru" id="ID" non',
        )
        self.assertEqual(with_html_stack.HTMLTag("a").text_attributes(), "")

    def test_text_error(self):
        with self.assertRaises(RuntimeError) as exc:
            self.assertEqual(
                with_html_stack.HTMLTag("!DOCTYPE").as_text(params=with_html_stack.PROD_PARAMS, raw="raw"), ""
            )
        self.assertEqual(
            str(exc.exception),
            'there may be no HTML in tag name starting with "!"',
        )

    def test_text(self):
        self.assertEqual(with_html_stack.HTMLTag("!a").as_text(params=with_html_stack.PROD_PARAMS), "<!a>")
        self.assertEqual(with_html_stack.HTMLTag("a").as_text(params=with_html_stack.PROD_PARAMS), "<a/>")
        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_text(params=with_html_stack.PROD_PARAMS), '<a color="red"/>'
        )

        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_text(
                params=with_html_stack.PROD_PARAMS, raw="I am\n<p>inner html</p>."
            ),
            '<a color="red">I am\n<p>inner html</p>.</a>',
        )
        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_text(
                params=with_html_stack.DEV_PARAMS, raw="I am\n<p>inner html</p>."
            ),
            """<a color="red">
I am
<p>inner html</p>.
</a>
""",
        )

    def test_code_attributes(self):
        self.assertEqual(
            with_html_stack.HTMLTag("a", href="http://&&.ru", _id="ID", non=None).code_attributes(),
            ", href='http://&&.ru', _id='ID', non=None",
        )
        self.assertEqual(
            with_html_stack.HTMLTag("a", href="http://&amp;&amp;.ru", _id="ID", non=None).code_attributes(),
            ", href=html.escape('http://&&.ru'), _id='ID', non=None",
        )
        self.assertEqual(with_html_stack.HTMLTag("a").code_attributes(), "")

    def test_code_error(self):
        with self.assertRaises(RuntimeError) as exc:
            self.assertEqual(
                with_html_stack.HTMLTag("!DOCTYPE").as_code(params=with_html_stack.PROD_PARAMS, raw="raw"), ""
            )
        self.assertEqual(
            str(exc.exception),
            'there may be no HTML in tag name starting with "!"',
        )

    def test_code(self):
        self.assertEqual(with_html_stack.HTMLTag("!a").as_code(params=with_html_stack.PROD_PARAMS), "doc('!a')")
        self.assertEqual(with_html_stack.HTMLTag("a").as_code(params=with_html_stack.PROD_PARAMS), "doc('a')")
        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_code(params=with_html_stack.PROD_PARAMS),
            "doc('a', color='red')",
        )

        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_code(
                params=with_html_stack.PROD_PARAMS, raw="I am\n<p>inner html</p>."
            ),
            "doc('a', color='red', raw='I am\\n<p>inner html</p>.')",
        )
        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_code(
                params=with_html_stack.DEV_PARAMS, raw="I am\n<p>inner html</p>."
            ),
            "doc('a', color='red', raw='I am\\n<p>inner html</p>.')\n",
        )

        # HTMLDocument prepares raw with proper indent
        self.assertEqual(
            with_html_stack.HTMLTag("a", color="red").as_code(
                params=with_html_stack.DEV_PARAMS, raw="I am\n<p>inner html</p>.", with_statement=True
            ),
            """with doc('a', color='red'):
I am
<p>inner html</p>.
""",
        )


class TestHTMLNode(unittest.TestCase):
    def test_root(self):
        node = with_html_stack.HTMLNode(tag=with_html_stack.HTMLTag("br"))
        self.assertIs(node.root(), node)

        node2 = with_html_stack.HTMLNode(parent=node, tag=with_html_stack.HTMLTag("tr"))
        node3 = with_html_stack.HTMLNode(parent=node2, tag=with_html_stack.HTMLTag("a"))
        self.assertIs(node3.root(), node)

    def test_verify_parent(self):
        node = with_html_stack.HTMLNode(tag=with_html_stack.HTMLTag("br"))
        node2 = with_html_stack.HTMLNode(parent=None, tag=with_html_stack.HTMLTag("tr"))
        node3 = with_html_stack.HTMLNode(parent=node, tag=with_html_stack.HTMLTag("tr"))
        node4 = with_html_stack.HTMLNode(parent="parent", tag=with_html_stack.HTMLTag("tr"))

        node2.verify()
        node3.verify()

        with self.assertRaises(RuntimeError) as exc:
            node4.verify()
        self.assertEqual(str(exc.exception), 'HTMLNode instance or None expected as "parent" parameter value')

    def test_verify_raw(self):
        node1 = with_html_stack.HTMLNode(raw=None)
        node2 = with_html_stack.HTMLNode(raw=with_html_stack.HTMLRaw("raw"))
        node3 = with_html_stack.HTMLNode(raw="raw")

        node1.verify()
        node2.verify()

        with self.assertRaises(RuntimeError) as exc:
            node3.verify()
        self.assertEqual(str(exc.exception), 'HTMLRaw instance expected as "raw" parameter value')

    def test_verify_tag(self):
        node1 = with_html_stack.HTMLNode(tag=None)
        node2 = with_html_stack.HTMLNode(tag=with_html_stack.HTMLTag("a"))
        node3 = with_html_stack.HTMLNode(tag="tag")

        node1.verify()
        node2.verify()

        with self.assertRaises(RuntimeError) as exc:
            node3.verify()
        self.assertEqual(str(exc.exception), 'HTMLTag instance expected as "tag" parameter value')

    def test_verify_children(self):
        node1 = with_html_stack.HTMLNode()
        node2 = with_html_stack.HTMLNode()
        node2.children = [with_html_stack.HTMLNode(tag="a")]
        node3 = with_html_stack.HTMLNode()
        node3.children = ["node", with_html_stack.HTMLNode(tag="a")]

        node1.verify()
        node2.verify()

        with self.assertRaises(RuntimeError) as exc:
            node3.verify()
        self.assertEqual(str(exc.exception), "HTMLNode instance expected as children item")

    def test_verify_other(self):
        node = with_html_stack.HTMLNode(raw=with_html_stack.HTMLRaw("raw"))
        node.children = [with_html_stack.HTMLNode(tag="a")]

        with self.assertRaises(RuntimeError) as exc:
            node.verify()
        self.assertEqual(str(exc.exception), "node can't contain HTML and children nodes at the same time")

    def test_text(self):
        node = with_html_stack.HTMLNode()
        self.assertEqual(node.as_text(params=with_html_stack.PROD_PARAMS), "")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        self.assertEqual(node.as_text(params=with_html_stack.PROD_PARAMS), '<a color="red"/>')

        node = with_html_stack.HTMLNode()
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(node.as_text(params=with_html_stack.PROD_PARAMS), "raw html")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(node.as_text(params=with_html_stack.PROD_PARAMS), '<a color="red">raw html</a>')

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(node.as_text(params=with_html_stack.DEV_PARAMS), '<a color="red">\n    raw html\n</a>\n')

        with self.assertRaises(RuntimeError) as exc:
            node = with_html_stack.HTMLNode()
            node.node_tag = with_html_stack.HTMLTag("a", color="red")
            node.node_raw = with_html_stack.HTMLRaw("raw html")
            node.children = [with_html_stack.HTMLNode()]
            self.assertEqual(node.as_text(params=with_html_stack.PROD_PARAMS), '<a color="red">raw html</a>')
        self.assertEqual(str(exc.exception), "node can't contain HTML and children nodes at the same time")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.children = [with_html_stack.HTMLNode(tag=with_html_stack.HTMLTag("br"))]
        self.assertEqual(node.as_text(params=with_html_stack.DEV_PARAMS), '<a color="red">\n    <br/>\n</a>\n')

    def test_code(self):
        node = with_html_stack.HTMLNode()
        self.assertEqual(node.as_code(params=with_html_stack.PROD_PARAMS), "")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        self.assertEqual(node.as_code(params=with_html_stack.PROD_PARAMS), "doc('a', color='red')")

        node = with_html_stack.HTMLNode()
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(node.as_code(params=with_html_stack.PROD_PARAMS), "raw html")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(node.as_code(params=with_html_stack.PROD_PARAMS), "doc('a', color='red', raw='raw html')")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.node_raw = with_html_stack.HTMLRaw("raw html")
        self.assertEqual(
            node.as_code(params=with_html_stack.DEV_PARAMS),
            "with doc('a', color='red'):\n    doc.raw('raw html')\n",
        )

        with self.assertRaises(RuntimeError) as exc:
            node = with_html_stack.HTMLNode()
            node.node_tag = with_html_stack.HTMLTag("a", color="red")
            node.node_raw = with_html_stack.HTMLRaw("raw html")
            node.children = [with_html_stack.HTMLNode()]
            self.assertEqual(node.as_code(params=with_html_stack.PROD_PARAMS), '<a color="red">raw html</a>')
        self.assertEqual(str(exc.exception), "node can't contain HTML and children nodes at the same time")

        node = with_html_stack.HTMLNode()
        node.node_tag = with_html_stack.HTMLTag("a", color="red")
        node.children = [with_html_stack.HTMLNode(tag=with_html_stack.HTMLTag("br"))]
        self.assertEqual(
            node.as_code(params=with_html_stack.DEV_PARAMS), "with doc('a', color='red'):\n    doc('br')\n"
        )


class TestHTMLDocument(unittest.TestCase):
    def setUp(self):
        doc = with_html_stack.HTMLDocument()
        with doc("html", lang="en"):
            with doc("head"):
                doc("title", raw="Example Domain")
                doc("meta", charset="utf-8")
            with doc("body"):
                with doc("div"):
                    doc("h1", raw="Example Domain")
                    with doc("p"):
                        doc.raw("This domain is for use in illustrative examples in documents. You ")
                        doc.raw(
                            "may use this domain in literature without prior coordination or asking for permission."
                        )
                    with doc("p"):
                        with doc("a", href="https://www.iana.org/domains/example"):
                            doc.raw("More information")
        self.doc = doc

    def test_text_dev(self):
        self.assertEqual(
            self.doc.as_text(with_html_stack.DEV_PARAMS),
            """\
<!DOCTYPE html>
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
""",
        )

    def test_text_prod(self):
        self.assertEqual(
            self.doc.as_text(with_html_stack.PROD_PARAMS),
            """\
<!DOCTYPE html><html lang="en"><head><title>Example Domain</title><meta charset="utf-8"/></head><body><div><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.</p><p><a href="https://www.iana.org/domains/example">More information</a></p></div></body></html>""",
        )

    def test_code(self):
        self.assertEqual(
            self.doc.as_code(),
            """\
doc('!DOCTYPE', html=None)
with doc('html', lang='en'):
    with doc('head'):
        with doc('title'):
            doc.raw('Example Domain')
        doc('meta', charset='utf-8')
    with doc('body'):
        with doc('div'):
            with doc('h1'):
                doc.raw('Example Domain')
            with doc('p'):
                doc.raw('This domain is for use in illustrative examples in documents. You ')
                doc.raw('may use this domain in literature without prior coordination or asking for permission.')
            with doc('p'):
                with doc('a', href='https://www.iana.org/domains/example'):
                    doc.raw('More information')
""",
        )

    def test_append(self):
        head = with_html_stack.HTMLDocument(doctype=False)
        with head("head"):
            head("title", raw="Example Domain")
            head("meta", charset="utf-8")

        content = with_html_stack.HTMLDocument(doctype=False)
        content("h1", raw="Example Domain")
        with content("p"):
            content.raw("This domain is for use in illustrative examples in documents. You ")
            content.raw("may use this domain in literature without prior coordination or asking for permission.")

        doc = with_html_stack.HTMLDocument()
        with doc("html", lang="en"):
            doc.append(head)
            with doc("body"):
                with doc("div"):
                    doc.append(content)
                    with doc("p"):
                        with doc("a", href="https://www.iana.org/domains/example"):
                            doc.raw("More information")

        self.assertEqual(
            doc.as_text(with_html_stack.DEV_PARAMS),
            """\
<!DOCTYPE html>
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
""",
        )
