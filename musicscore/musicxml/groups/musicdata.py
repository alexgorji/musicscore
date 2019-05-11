from musicscore.musicxml.elements.barline import Barline
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.elements.note import Note
from musicscore.musicxml.types.complextypes.attributes import ComplexTypeAttributes
from musicscore.musicxml.types.complextypes.backup import ComplexTypeBackup
from musicscore.musicxml.types.complextypes.direction import ComplexTypeDirection
from musicscore.musicxml.types.complextypes.sound import ComplexTypeSound


class Backup(ComplexTypeBackup):
    _TAG = 'backup'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Forward(XMLElement):
    _TAG = 'forward'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        NotImplementedError()


class Direction(ComplexTypeDirection):
    _TAG = 'direction'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Attributes(ComplexTypeAttributes):
    _TAG = 'attributes'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Sound(ComplexTypeSound):
    _TAG = 'sound'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Link(XMLElement):
    _TAG = 'link'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        NotImplementedError()


class Bookmark(XMLElement):
    _TAG = 'bookmark'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)
        NotImplementedError()


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
