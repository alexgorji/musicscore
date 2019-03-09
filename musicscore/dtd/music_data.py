from musicscore.musicxml.elements.xml_element import XMLElement, XMLElementGroup
from musicscore.dtd.dtd import Group, Sequence, Choice, Element
from musicscore.dtd.note import Note
import copy


class Backup(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='backup', *args, **kwargs)


class Forward(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='forward', *args, **kwargs)


class Direction(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='direction', *args, **kwargs)


class Attributes(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='attributes', *args, **kwargs)


class Sound(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='sound', *args, **kwargs)


class Barline(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)


class Link(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='link', *args, **kwargs)


class Bookmark(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='bookmark', *args, **kwargs)


class MusicData(XMLElementGroup):
    """"""

    _DTD = Sequence(
        Choice(
            Element(Note),
            Element(Backup),
            Element(Forward),
            Element(Direction),
            Element(Attributes),
            Element(Sound),
            Element(Barline),
            Element(Link),
            Element(Bookmark),
            min_occurrence=0,
            max_occurrence=None
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtd = copy.copy(self._DTD)

    def reset_children(self):
        self.clear_children()
        self.dtd._possibility_index = 0

    def add_child(self, child):
        self.dtd.check_child_type(self, child)
        self.dtd.check_child_max_occurrence(self, child)
        self._children.append(child)
        return child

    def sort_children(self):
        self.dtd.sort_children(self)

    def close(self):
        self.dtd.close(self)
