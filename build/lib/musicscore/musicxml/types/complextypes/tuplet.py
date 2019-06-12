from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, NonNegativeInteger, TypeNoteTypeValue
from musicscore.musicxml.attributes.color import Color
from musicscore.musicxml.attributes.font import Font
from musicscore.musicxml.attributes.lineshape import LineShape
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeNumberLevel, TypeStartStop


class TupletDot(XMLElement, Font, Color):
    """
    The tuplet-dot type is used to specify dotted normal tuplet types.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='tuplet-dot', *args, **kwargs)


class TupletNumber(XMLElement, NonNegativeInteger, Font, Color):
    """
    The tuplet-number type indicates the number of notes for this portion of the tuplet.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='tuplet-number', value=value, *args, **kwargs)


class TupletType(XMLElement, TypeNoteTypeValue, Font, Color):
    """
	The tuplet-type type indicates the graphical note type of the notes for this portion of the tuplet.</xs:documentation>
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='tuplet-type', value=value, *args, **kwargs)


class ComplexTypeTupletPortion(ComplexType):
    """
    The tuplet-portion type provides optional full control over tuplet specifications. It allows the number and note
    type (including dots) to be set for the actual and normal portions of a single tuplet. If any of these elements are
    absent, their values are based on the time-modification element.
    """
    _DTD = Sequence(
        Element(TupletNumber, min_occurrence=0),
        Element(TupletType, min_occurrence=0),
        Element(TupletDot, min_occurrence=0, max_occurrence=None)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class TupletActual(ComplexTypeTupletPortion):
    """
    The tuplet-actual element provide optional full control over how the actual part of the tuplet is displayed,
    including number and note type (with dots). If any of these elements are absent, their values are based on the
    time-modification element.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='tuplet-actual', value=value, *args, **kwargs)


class TupletNormal(ComplexTypeTupletPortion):
    """
    The tuplet-normal element provide optional full control over how the normal part of the tuplet is displayed,
    including number and note type (with dots). If any of these elements are absent, their values are based on the
    time-modification element.
    """

    def __init__(self, value=None, *args, **kwargs):
        super().__init__(tag='tuplet-normal', value=value, *args, **kwargs)


class Bracket(AttributeAbstract):
    def __init__(self, bracket=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('bracket', bracket, 'TypeYesNo')


class ShowNumber(AttributeAbstract):
    def __init__(self, show_number=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('show-number', show_number, 'TypeShowTuplet')


class ShowType(AttributeAbstract):
    def __init__(self, show_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('show-type', show_type, 'TypeShowTuplet')


class ComplexTypeTuplet(ComplexType, Bracket, ShowNumber, ShowType, LineShape, Position, Placement, OptionalUniqueId):
    """
    A tuplet element is present when a tuplet is to be displayed graphically, in addition to the sound data provided by
    the time-modification elements. The number attribute is used to distinguish nested tuplets. The bracket attribute is
    used to indicate the presence of a bracket. If unspecified, the results are implementation-dependent. The line-shape
    attribute is used to specify whether the bracket is straight or in the older curved or slurred style. It is straight
    by default.

    Whereas a time-modification element shows how the cumulative, sounding effect of tuplets and double-note tremolos
    compare to the written note type, the tuplet element describes how this is displayed. The tuplet element also
    provides more detailed representation information than the time-modification element, and is needed to represent
    nested tuplets and other complex tuplets accurately.

    The show-number attribute is used to display either the number of actual notes, the number of both actual and normal
    notes, or neither. It is actual by default. The show-type attribute is used to display either the actual type, both
    the actual and normal types, or neither. It is none by default.
    """
    _DTD = Sequence(
        Element(TupletActual, min_occurrence=0),
        Element(TupletNormal, min_occurrence=0)
    )

    def __init__(self, type, number=1, *args, **kwargs):
        super().__init__(tag='tuplet', *args, **kwargs)
        self.type = type
        self.number = number

    @property
    def number(self):
        return self.get_attribute('number')

    @number.setter
    def number(self, value):
        if value is None:
            self.remove_attribute('number')
        else:
            TypeNumberLevel(value)
            self._ATTRIBUTES.insert(0, 'number')
            self.set_attribute('number', value)

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            TypeStartStop(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
