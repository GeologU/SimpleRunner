import unittest

import html_attributes_global
from html_attributes_global import global_attribute


class TestAttributeBase(unittest.TestCase):

    def assertGoodValue(self, good_value, internal=None):
        if internal is None:
            internal = good_value
        self.assertEqual(
            str(self.attr_cls(good_value)),
            ' {}="{}"'.format(self.attr_cls.ATTR, internal)
        )

    def assertBadValue(self, bad_value, internal=None):
        if internal is None:
            internal = bad_value
        with self.assertRaises(ValueError) as exc:
            self.attr_cls(bad_value)

        self.assertEqual(
            exc.exception.args[0],
            'Bad value for attribute {}: {}'.format(self.attr_cls.ATTR, repr(internal))
        )


class TestAttributeAccessKey(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeAccessKey

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('x')), ' accesskey="x"')

    def test_good(self):
        self.assertGoodValue('a')
        self.assertGoodValue('h')
        self.assertGoodValue('z')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('H')
        self.assertBadValue('h5')
        self.assertBadValue('')


class TestAttributeClass(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeClass

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('intro')), ' class="intro"')

    def test_good(self):
        self.assertGoodValue('i')
        self.assertGoodValue('i v')
        self.assertGoodValue('intro')
        self.assertGoodValue('intro important')

    def test_bad(self):
        self.assertBadValue(None)                # non-string
        self.assertBadValue('int:ro')            # wrong character :
        self.assertBadValue(' intro')            # leading space
        self.assertBadValue('intro ')            # trailing space
        self.assertBadValue('5intro')            # leading non-alpha
        self.assertBadValue('intro  important')  # 2 spaces
        self.assertBadValue('intro intro')       # repeat


class TestAttributeContentEditable(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeContentEditable

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('false')), ' contenteditable="false"')

    def test_good(self):
        self.assertGoodValue('true')
        self.assertGoodValue('false')
        self.assertGoodValue(True, 'true')
        self.assertGoodValue(False, 'false')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('')
        self.assertBadValue('False')
        self.assertBadValue('True')
        self.assertBadValue('editable')


class TestAttributeDataStar(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeDataStar

    def assertGoodName(self, good_name, internal=None):
        if internal is None:
            internal = good_name
        self.assertEqual(
            str(self.attr_cls(good_name, 'somevalue')),
            ' {}="somevalue"'.format(internal)
        )

    def assertBadName(self, bad_name):
        with self.assertRaises(ValueError) as exc:
            self.attr_cls(bad_name, 'somevalue')

        if isinstance(bad_name, str) and not bad_name.startswith('data-'):
            bad_name = 'data-' + bad_name

        self.assertEqual(
            exc.exception.args[0],
            'Bad name for attribute {}: {}'.format(self.attr_cls.ATTR, repr(bad_name))
        )

    def test_name_good(self):
        self.assertGoodName('data', 'data-data')
        self.assertGoodName('x', 'data-x')
        self.assertGoodName('nice-lemon-tree', 'data-nice-lemon-tree')
        self.assertGoodName('data-nice-lemon-tree')

    def test_name_bad(self):
        self.assertBadName(None)
        self.assertBadName(5)
        self.assertBadName('')
        self.assertBadName('9')
        self.assertBadName('data-')
        self.assertBadName('dAta-')
        self.assertBadName('san_andreas')
        self.assertBadName('StPeter')
        self.assertBadName('olga2')

    def test_value_good(self):
        self.assertEqual(
            str(self.attr_cls('test', 'any string is a good value')),
            ' data-test="any string is a good value"'
        )
        self.assertEqual(
            str(self.attr_cls('data-test', '')),
            ' data-test=""'
        )

    def test_value_bad(self):
        with self.assertRaises(ValueError) as exc:
            self.attr_cls('test', None)
        self.assertEqual(
            exc.exception.args[0],
            'Bad value for attribute data-test: None'
        )

        with self.assertRaises(ValueError) as exc:
            self.attr_cls('test', 42)
        self.assertEqual(
            exc.exception.args[0],
            'Bad value for attribute data-test: 42'
        )


class TestAttributeDir(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeDir

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('auto')), ' dir="auto"')

    def test_good(self):
        self.assertGoodValue('ltr')
        self.assertGoodValue('rtl')
        self.assertGoodValue('auto')
        self.assertGoodValue(None, 'auto')

    def test_bad(self):
        self.assertBadValue('')
        self.assertBadValue('direction')


class TestAttributeDraggable(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeDraggable

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('auto')), ' draggable="auto"')

    def test_good(self):
        self.assertGoodValue('true')
        self.assertGoodValue('false')
        self.assertGoodValue('auto')
        self.assertGoodValue(True, 'true')
        self.assertGoodValue(False, 'false')
        self.assertGoodValue(None, 'auto')

    def test_bad(self):
        self.assertBadValue('')
        self.assertBadValue('False')
        self.assertBadValue('True')


class TestAttributeDropZone(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeDropZone

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('copy')), ' dropzone="copy"')

    def test_good(self):
        self.assertGoodValue('copy')
        self.assertGoodValue('move')
        self.assertGoodValue('link')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('')
        self.assertBadValue('cp')
        self.assertBadValue(2)


class TestAttributeHidden(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeHidden

    def test_attr(self):
        self.assertEqual(str(self.attr_cls()), ' hidden')


class TestAttributeID(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeID

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('some_id')), ' id="some_id"')

    def test_good(self):
        self.assertGoodValue('4')
        self.assertGoodValue('i')
        self.assertGoodValue('something')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue(4)
        self.assertBadValue('')
        self.assertBadValue('some thing')
        self.assertBadValue('some\tthing')


class TestAttributeLang(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeLang

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('en')), ' lang="en"')
        self.assertEqual(len(self.attr_cls.ISO_LANGUAGE_CODES), 189)

    def test_good(self):
        self.assertGoodValue('ab')
        self.assertGoodValue('zu')
        self.assertGoodValue('en')
        self.assertGoodValue('zh-Hant')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('')
        self.assertBadValue('EN')
        self.assertBadValue('eng')


class TestAttributeSpellCheck(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeSpellCheck

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('false')), ' spellcheck="false"')

    def test_good(self):
        self.assertGoodValue('true')
        self.assertGoodValue('false')
        self.assertGoodValue(True, 'true')
        self.assertGoodValue(False, 'false')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('')
        self.assertBadValue('False')
        self.assertBadValue('True')
        self.assertBadValue('spellcheck')


class TestAttributeStyle(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeStyle

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('style_definitions')), ' style="style_definitions"')

    def test_good(self):
        self.assertGoodValue('')
        self.assertGoodValue('some style')

    def test_bad(self):
        self.assertBadValue(None)


class TestAttributeTabIndex(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeTabIndex

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('5')), ' tabindex="5"')

    def test_good(self):
        self.assertGoodValue(1)
        self.assertGoodValue('1')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue(0, '0')
        self.assertBadValue('one')
        self.assertBadValue('-1')
        self.assertBadValue('1.5')


class TestAttributeTitle(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeTitle

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('text')), ' title="text"')

    def test_good(self):
        self.assertGoodValue('')
        self.assertGoodValue('A tooltip text for an element')

    def test_bad(self):
        self.assertBadValue(None)


class TestAttributeTranslate(TestAttributeBase):

    @classmethod
    def setUpClass(cls):
        cls.attr_cls = html_attributes_global.AttributeTranslate

    def test_attr(self):
        self.assertEqual(str(self.attr_cls('yes')), ' translate="yes"')

    def test_good(self):
        self.assertGoodValue('yes')
        self.assertGoodValue('no')
        self.assertGoodValue(True, 'yes')
        self.assertGoodValue(False, 'no')

    def test_bad(self):
        self.assertBadValue(None)
        self.assertBadValue('')
        self.assertBadValue('Yes')
        self.assertBadValue('No')
        self.assertBadValue('translate')


class TestGlobalAttribute(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(len(html_attributes_global.GLOBAL_ATTRIBUTE_BY_NAME), 15)

        self.assertIsInstance(global_attribute('accesskey', 'a'),
                              html_attributes_global.AttributeAccessKey)
        self.assertIsInstance(global_attribute('class', 'test'),
                              html_attributes_global.AttributeClass)
        self.assertIsInstance(global_attribute('contenteditable', 'true'),
                              html_attributes_global.AttributeContentEditable)
        self.assertIsInstance(global_attribute('data-test', 'test'),
                              html_attributes_global.AttributeDataStar)
        self.assertIsInstance(global_attribute('dir', 'auto'),
                              html_attributes_global.AttributeDir)
        self.assertIsInstance(global_attribute('draggable', 'auto'),
                              html_attributes_global.AttributeDraggable)
        self.assertIsInstance(global_attribute('dropzone', 'link'),
                              html_attributes_global.AttributeDropZone)
        self.assertIsInstance(global_attribute('hidden'),
                              html_attributes_global.AttributeHidden)
        self.assertIsInstance(global_attribute('id', 'id'),
                              html_attributes_global.AttributeID)
        self.assertIsInstance(global_attribute('lang', 'fr'),
                              html_attributes_global.AttributeLang)
        self.assertIsInstance(global_attribute('spellcheck', 'true'),
                              html_attributes_global.AttributeSpellCheck)
        self.assertIsInstance(global_attribute('style', 'test'),
                              html_attributes_global.AttributeStyle)
        self.assertIsInstance(global_attribute('tabindex', '4'),
                              html_attributes_global.AttributeTabIndex)
        self.assertIsInstance(global_attribute('title', 'test'),
                              html_attributes_global.AttributeTitle)
        self.assertIsInstance(global_attribute('translate', 'yes'),
                              html_attributes_global.AttributeTranslate)

        self.assertIsNone(global_attribute('nothing', 'test'))

        with self.assertRaises(ValueError) as exc:
            global_attribute('hidden', 'test')
        self.assertEqual(
            exc.exception.args[0],
            "Got value where None is expected: 'test'",
        )
