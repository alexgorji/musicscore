from musicscore.musicxml.elements.barline import Barline
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.elements.note import Note
from musicscore.musicxml.types.complextypes.backup import ComplexTypeBackup


class Backup(ComplexTypeBackup):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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


class Link(XMLElement):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='link', *args, **kwargs)


class Bookmark(XMLElement):
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
