from musicscore.musicxml.elements.xml_element import XMLElement2
from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.elements.note import Note


class Backup(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='backup', *args, **kwargs)


class Forward(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='forward', *args, **kwargs)


class Direction(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='direction', *args, **kwargs)


class Attributes(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='attributes', *args, **kwargs)


class Sound(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='sound', *args, **kwargs)


class Barline(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)


class Link(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='link', *args, **kwargs)


class Bookmark(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='bookmark', *args, **kwargs)


MusicData = Sequence(
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
