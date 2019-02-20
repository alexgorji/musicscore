from unittest import TestCase
from musicscore.musicxml.elements.xml_element import XMLElement, XMLElementGroup


class TestSortChildren(TestCase):
    def setUp(self):
        class A(XMLElement):
            """"""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        class B(XMLElementGroup):
            """"""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        class BGroup(XMLElementGroup):
            """"""
            _CHILDREN_TYPES = [B]

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        class C(XMLElement):
            """"""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        class D(XMLElement):
            """"""
            _CHILDREN_TYPES = [BGroup, C, A]

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
