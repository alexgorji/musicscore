from musicscore.dtd.dtd import Sequence, Group, Element, Choice
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.elements.editorial import Editorial
from musicscore.musicxml.elements.xml_element import XMLElement, XMLElement2
from musicscore.musicxml.types.complex_type import TypeKey
from musicscore.musicxml.types.simple_type import PositiveDivisions, ClefSign, StaffLine, PositiveInteger
from musicscore.musicxml.attributes.print_object import PrintObject


class Divisions(XMLElement2, PositiveDivisions):
    """
    Musical notation duration is commonly represented as fractions.
    The divisions element indicates how many divisions per quarter note are used to indicate a note's duration.
    For example, if duration = 1 and divisions = 2, this is an eighth note duration.
    Duration and divisions are used directly for generating sound output, so they must be chosen to take tuplets into
    account. Using a divisions element lets us use just one number to represent a duration for each note in the score,
    while retaining the full power of a fractional representation.
    If maximum compatibility with Standard MIDI 1.0 files is important, do not have the divisions value exceed 16383.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='divisions', value=value, *args, **kwargs)


class Key(TypeKey):
    """
    The key element represents a key signature. Both traditional and non-traditional key signatures are supported.
    The optional number attribute refers to staff numbers. If absent, the key signature applies to all staves in the
    part.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='key', value=value, *args, **kwargs)


class Beats(XMLElement2, PositiveInteger):
    """
    The beats element indicates the number of beats, as found in the numerator of a time signature.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='beats', value=value, *args, **kwargs)


class BeatType(XMLElement2, PositiveInteger):
    """
    The beat-type element indicates the beat unit, as found in the denominator of a time signature.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='beat-type', value=value, *args, **kwargs)


TimeSignature = Sequence(
    Element(Beats),
    Element(BeatType)
)


class Interchangeable(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='interchangeable', *args, **kwargs)
        raise NotImplementedError()


class SenzaMisura(XMLElement2):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='senza-misura', *args, **kwargs)
        raise NotImplementedError()


# todo:	<xs:attribute name="number" type="staff-number"/>
# 		<xs:attribute name="symbol" type="time-symbol"/>
# 		<xs:attribute name="separator" type="time-separator"/>
# 		<xs:attributeGroup ref="print-style-align"/>

# , OptionalUniqueId
class Time(XMLElement2, PrintObject, OptionalUniqueId):
    """
    Time signatures are represented by the beats element for the numerator and the beat-type element for the
    denominator. The symbol attribute is used indicate common and cut time symbols as well as a single number display.
    Multiple pairs of beat and beat-type elements are used for composite time signatures with multiple denominators,
    such as 2/4 + 3/8. A composite such as 3+2/8 requires only one beat/beat-type pair.
    The print-object attribute allows a time signature to be specified but not printed, as is the case for excerpts
    from the middle of a score. The value is "yes" if not present. The optional number attribute refers to staff numbers
    within the part. If absent, the time signature applies to all staves in the part.
    """

    _DTD = Choice(
        Sequence(
            Group(TimeSignature, max_occurrence=None),
            Element(Interchangeable, min_occurrence=0)
        ),
        Element(SenzaMisura)
    )

    # _ATTRIBUTES = ['print-object']

    def __init__(self, *args, **kwargs):
        super().__init__(tag='time', *args, **kwargs)


class Staves(XMLElement2):
    """
    The staves element is used if there is more than one staff represented in the given part (e.g., 2 staves for typical
    piano parts). If absent, a value of 1 is assumed. Staves are ordered from top to bottom in a part in numerical
    order, with staff 1 above staff 2

        </xs:element>
    <xs:element name="staves" type="xs:nonNegativeInteger" minOccurs="0">
    </xs:element>

    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='staves', value=value, *args, **kwargs)
        raise NotImplementedError()


class PartSymbol(XMLElement2):
    """
    The part-symbol element indicates how a symbol for a multi-staff part is indicated in the score.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='part-symbols', value=value, *args, **kwargs)
        raise NotImplementedError()


class Instruments(XMLElement2):
    """
    <xs:element name="instruments" type="xs:nonNegativeInteger" minOccurs="0">
      <xs:annotation>
        <xs:documentation>The instruments element is only used if more than one instrument is represented in the part (e.g., oboe I and II where they play together most of the time). If absent, a value of 1 is assumed.</xs:documentation>
      </xs:annotation>
    </xs:element>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='instruments', value=value, *args, **kwargs)
        raise NotImplementedError()


class Clef(XMLElement2):
    """
    Clefs are represented by a combination of sign, line, and clef-octave-change elements.
    The optional number attribute refers to staff numbers within the part.
    A value of 1 is assumed if not present.
    Sometimes clefs are added to the staff in non-standard line positions, either to indicate cue passages,
    or when there are multiple clefs present simultaneously on one staff. In this situation,
    the additional attribute is set to "yes" and the line value is ignored.
    The size attribute is used for clefs where the additional attribute is "yes".
    It is typically used to indicate cue clefs.

    Sometimes clefs at the start of a measure need to appear after the barline rather than before,
    as for cues or for use after a repeated section.
    The after-barline attribute is set to "yes" in this situation. The attribute is ignored for mid-measure clefs.

    Clefs appear at the start of each system unless the print-object attribute has been set to "no" or
    the additional attribute has been set to "yes"
    """

    class Sign(XMLElement2, ClefSign):
        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='sign', value=value, *args, **kwargs)

    class Line(XMLElement2, StaffLine):
        def __init__(self, value, *args, **kwargs):
            super().__init__(tag='line', value=value, *args, **kwargs)

    def __init__(self, sign, line):
        super().__init__(tag='clef')
        self._sign = None
        self._line = None
        self.sign = sign
        self.line = line

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, value):
        self._set_child(self.XMLSign, 'sign', value)

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        self._set_child(self.XMLLine, 'line', value)


class StaffDetails(XMLElement2):
    """
    <xs:element name="staff-details" type="staff-details" minOccurs="0" maxOccurs="unbounded">
      <xs:annotation>
        <xs:documentation>The staff-details element is used to indicate different types of staves.</xs:documentation>
      </xs:annotation>
    </xs:element>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='staff-details', value=value, *args, **kwargs)
        raise NotImplementedError()


class Transpose(XMLElement2):
    """
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='transpose', value=value, *args, **kwargs)
        raise NotImplementedError()


class Directive(XMLElement2):
    """
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='directive', value=value, *args, **kwargs)
        raise NotImplementedError()


class MeasureStyle(XMLElement2):
    """
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='measure-style', value=value, *args, **kwargs)
        raise NotImplementedError()


class Attributes(XMLElement2):
    """
    The attributes element contains musical information that typically changes on measure boundaries. This includes key
    and time signatures, clefs, transpositions, and staving. When attributes are changed mid-measure, it affects the
    music in score order, not in MusicXML document order
    """
    _DTD = Sequence(
        Group(Editorial),
        Element(Divisions, min_occurrence=0),
        Element(Key, min_occurrence=0, max_occurrence=None),
        Element(Time, min_occurrence=0, max_occurrence=None),
        Element(Staves, min_occurrence=0),
        Element(PartSymbol, min_occurrence=0),
        Element(Instruments, min_occurrence=0),
        Element(Clef, min_occurrence=0),
        Element(StaffDetails, min_occurrence=0, max_occurrence=None),
        Element(Transpose, min_occurrence=0, max_occurrence=None),
        Element(Directive, min_occurrence=0, max_occurrence=None),
        Element(MeasureStyle, min_occurrence=0, max_occurrence=None)

    )

    def __init__(self):
        super().__init__(tag='attributes')
