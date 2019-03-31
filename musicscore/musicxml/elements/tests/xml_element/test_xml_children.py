from unittest import TestCase

from musicscore.dtd.dtd import Sequence, Element, ChildOccurrenceDTDConflict, ChildTypeDTDConflict
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.exceptions import ChildAlreadyExists


class A(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='a', *args, **kwargs)
        self.multiple = True


class B(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='b', *args, **kwargs)


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
    _DTD=Sequence(
        Element(C),
        Element(A, max_occurrence=None),
        Element(B)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='e', *args, **kwargs)


class TestAddChildren(TestCase):

    def test_add_child(self):
        e = E()
        e.add_child(C())
        # with self.assertRaises(ChildTypeDTDConflict):
        #     e.add_child(D())
        # self.assertEqual(len(e.get_children()), 1)
        # self.assertEqual(type(e.get_children()[0]), C)

    def test_add_multiple_child(self):
        e = E()
        e.add_child(A())
        e.add_child(C())
        e.add_child(A())
        e.add_child(A())
        self.assertEqual(len(e.get_children_by_type(A)), 3)
        self.assertEqual(len(e.get_children_by_type(C)), 1)
        self.assertEqual(len(e.get_children_by_type(D)), 0)

    def test_non_multiple_child(self):
        e = E()
        e.add_child(C())
        with self.assertRaises(ChildOccurrenceDTDConflict):
            e.add_child(C())


    def test_sort_children(self):
        e = E()
        e.add_child(A())
        e.add_child(B())
        e.add_child(A())
        e.add_child(C())
        result = [C, A, A, B]
        self.assertEqual([type(child) for child in e.get_children()], result)

    # def test_access_child(self):
    #     e = E()
    #     e.add_child(A())
    #     e.add_child(B())
    #     e.add_child(A())
    #     e.add_child(C())
    #
    #     self.assertEqual([type(child) for child in e.a], [A, A])
    #     self.assertEqual(type(e.b), B)
    #     with self.assertRaises(AttributeError):
    #         print(e.d)
