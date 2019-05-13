from musicscore.musicxml.elements.barline import Barline
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.dtd.dtd import Sequence, Choice, Element
from musicscore.musicxml.elements.note import Note
from musicscore.musicxml.types.complextypes.attributes import ComplexTypeAttributes
from musicscore.musicxml.types.complextypes.backup import ComplexTypeBackup
from musicscore.musicxml.types.complextypes.direction import ComplexTypeDirection
from musicscore.musicxml.types.complextypes.sound import ComplexTypeSound
from musicscore.musicxml.types.complextypes.print import ComplexTypePrint


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


class Print(ComplexTypePrint):
    _TAG = 'print'

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
        Element(Print),
        Element(Sound),
        Element(Barline),
        Element(Link),
        Element(Bookmark),
        min_occurrence=0,
        max_occurrence=None
    )
)

'''
                <xs:element name="note" type="note"/>
                <xs:element name="backup" type="backup"/>
                <xs:element name="forward" type="forward"/>
                <xs:element name="direction" type="direction"/>
                <xs:element name="attributes" type="attributes"/>
                <xs:element name="harmony" type="harmony"/>
                <xs:element name="figured-bass" type="figured-bass"/>
                <xs:element name="print" type="print"/>
                <xs:element name="sound" type="sound"/>
                <xs:element name="barline" type="barline"/>
                <xs:element name="grouping" type="grouping"/>
                <xs:element name="link" type="link"/>
                <xs:element name="bookmark" type="bookmark"/>
'''
