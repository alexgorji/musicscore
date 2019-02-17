from musicscore.musicxml.elements.xml_element import XMLElement


class ComplexType(object):
    def __init__(self):
        pass


# TODO: add exception for attributes
class Empty(ComplexType, XMLElement):
    """
    Empty is a type of XMLElement with no children, no text and no attributes
    """

    def __init__(self, tag):
        XMLElement.__init__(self, tag=tag)

    def add_child(self, child):
        raise Exception('Empty cannot have children.')

    @XMLElement.text.setter
    def text(self, value):
        raise Exception('Empty cannot have text.')


# class EmptyPlacement(Empty, PrintStyle, Placement):
# todo: PrintStyle and Placement
class EmptyPlacement(Empty):
    """
    The empty-placement type represents an empty element with print-style and placement attributes
    """

    def __init__(self, tag):
        super().__init__(self, tag=tag)
