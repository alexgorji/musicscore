from musicscore.dtd.dtd import Sequence, Choice, Element, GroupReference
from musicscore.musicxml.attributes.attribute_abstract import TypeSyllabic
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.justify import Justify
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.timeonly import TimeOnly
from musicscore.musicxml.groups.common import Editorial, FootNote
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.complextypes.elision import ComplexTypeElision
from musicscore.musicxml.types.complextypes.extend import ComplexTypeExtend
from musicscore.musicxml.types.complextypes.textelementdata import ComplexTypeTextElementData
from unittest import TestCase

from musicscore.musicxml.types.simple_type import Token


class Syllabic(XMLElement, TypeSyllabic):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='syllabic', value=value, *args, **kwargs)


class Text(ComplexTypeTextElementData):
    """"""

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='text', value=value, *args, **kwargs)


class Elision(ComplexTypeElision):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='elision', *args, **kwargs)


class Extend(ComplexTypeExtend):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='extend', *args, **kwargs)


class Laughing(Empty):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='laughing', *args, **kwargs)


class Humming(Empty):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='humming', *args, **kwargs)


class EndParagraph(Empty):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='end-paragraph', *args, **kwargs)


class EndLine(Empty):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='end-line', *args, **kwargs)


class ComplexTypeLyric(ComplexType, Justify, Position, Placement, Color, PrintObject, TimeOnly,
                       OptionalUniqueId):
    """The lyric type represents text underlays for lyrics, based on Humdrum with support for other formats. Two text
    elements that are not separated by an elision element are part of the same syllable, but may have different text
    formatting. The MusicXML XSD is more strict than the DTD in enforcing this by disallowing a second syllabic element
    unless preceded by an elision element. The lyric number indicates multiple lines, though a name can be used as well
    (as in Finale's verse / chorus / section specification).

    Justification is center by default; placement is below by default. The print-object attribute can override a note's
    print-lyric attribute in cases where only some lyrics on a note are printed, as when lyrics for later verses are
    printed in a block of text rather than with each note. The time-only attribute precisely specifies which lyrics are
    to be sung which time through a repeated section.
    """

    # todo: sorting mixed Sequence with min_occurrence = 0 and max_occurrence = None and check_occurrence.
    #  Syllabic doubled by sort
    _DTD = Sequence(
        Choice(
            Sequence(
                Element(Syllabic, min_occurrence=0),
                Element(Text),
                # Sequence(
                #     Sequence(
                #         Element(Elision),
                #         Element(Syllabic, min_occurrence=0),
                #         min_occurrence=0
                #     ),
                #     Element(Text)
                #     # ,
                #     # min_occurrence=0,
                #     # max_occurrence=None
                # ),
                Element(Extend, min_occurrence=0)
            ),
            Element(Extend),
            Element(Laughing),
            Element(Humming)
        ),
        Element(EndLine, min_occurrence=0),
        Element(EndParagraph, min_occurrence=0),
        GroupReference(Editorial)
    )

    def __init__(self, number='1', *args, **kwargs):
        super().__init__(tag='lyric', *args, **kwargs)
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

    @property
    def name(self):
        return self.get_attribute('name')

    @name.setter
    def name(self, value):
        if value is None:
            self.remove_attribute('name')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'name')
            self.set_attribute('name', value)