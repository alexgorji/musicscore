from unittest import TestCase
from musicscore.musicxml.elements.xml_element import XMLElement


class A(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='a', *args, **kwargs)


class B(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='b', *args, **kwargs)
        self.multiple = True


class C(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='c', *args, **kwargs)


class D(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='d', *args, **kwargs)


class E(XMLElement):
    """"""
    _CHILDREN_TYPES = [B, C, A]

    def __init__(self, *args, **kwargs):
        super().__init__(tag='e', *args, **kwargs)


class TestSortChildren(TestCase):

    def test_add_child(self):
        e = E()
        e.add_child(C())
        with self.assertRaises(TypeError):
            e.add_child(D())
        self.assertEqual(len(e.get_children()), 1)
        self.assertEqual(type(e.get_children()[0]), C)

    def test_add_multiple_child(self):
        e = E()
        e.add_child(C())
        with self.assertRaises(TypeError):
            e.add_child(D())
        self.assertEqual(len(e.get_children()), 1)
        self.assertEqual(type(e.get_children()[0]), C)
