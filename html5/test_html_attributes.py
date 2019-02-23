import unittest

from html_attributes import quote, Attribute


class TestQuote(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(quote('text'), '"text"')
        self.assertEqual(quote('"secret" text'), "'\"secret\" text'")
        self.assertEqual(quote(''''special' "secret" text'''), '''"'special' \\"secret\\" text"''')


class TestAttribute(unittest.TestCase):

    def test_basic(self):
        a = Attribute('src', 'img_typo.jpg')
        self.assertEqual(str(a), ' src="img_typo.jpg"')

        a = Attribute('alt', 'Girl with a jacket')
        self.assertEqual(str(a), ' alt="Girl with a jacket"')

        a = Attribute('href', 'https://www.w3schools.com')
        self.assertEqual(str(a), ' href="https://www.w3schools.com"')

        a = Attribute('title', "I'm a tooltip")
        self.assertEqual(str(a), ' title="I\'m a tooltip"')

        a = Attribute('style', "color:red")
        self.assertEqual(str(a), ' style="color:red"')

    def test_validate(self):
        with self.assertRaises(ValueError) as exc:
            Attribute('test', None)
        self.assertEqual(exc.exception.args[0], 'Bad value for attribute test: None')

        with self.assertRaises(ValueError) as exc:
            Attribute('test', 4)
        self.assertEqual(exc.exception.args[0], 'Bad value for attribute test: 4')
