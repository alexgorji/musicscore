from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.bracket import ComplexTypeBracket
from musicscore.musicxml.types.complextypes.coda import ComplexTypeCoda
from musicscore.musicxml.types.complextypes.complextype import ComplexType, EmptyPrintStyleAlignId
from musicscore.musicxml.types.complextypes.dynamics import ComplexTypeDynamics, Dynamics
from musicscore.musicxml.types.complextypes.formattedsymbolid import ComplexTypeFormattedSymbolId
from musicscore.musicxml.types.complextypes.formattedtextid import ComplexTypeFormattedTextId
from musicscore.musicxml.types.complextypes.metronome import ComplexTypeMetronome
from musicscore.musicxml.types.complextypes.segno import ComplexTypeSegno
from musicscore.musicxml.types.complextypes.wedge import ComplexTypeWedge


class Rehearsal(ComplexTypeFormattedTextId):
    """The rehearsal type specifies a rehearsal mark. Language is Italian ("it") by default. Enclosure is square by
    default. Left justification is assumed if not specified.
    """
    _TAG = 'rehearsal'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Segno(ComplexTypeSegno):
    _TAG = 'segno'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Coda(ComplexTypeCoda):
    _TAG = 'coda'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Words(ComplexTypeFormattedTextId):
    """
    The words element specifies a standard text direction. Left justification is assumed if not specified. Language is
    Italian ("it") by default. Enclosure is none by default.
    """
    _TAG = 'words'

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Symbol(ComplexTypeFormattedSymbolId):
    """
    The symbol element specifies a musical symbol using a canonical SMuFL glyph name. It is used when an occasional
    musical symbol is interspersed into text. It should not be used in place of semantic markup, such as metronome
    marks that mix text and symbols. Left justification is assumed if not specified. Enclosure is none by default.
    """
    _TAG = 'symbol'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Wedge(ComplexTypeWedge):
    _TAG = 'wedge'

    def __init__(self, type, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Dashes(XMLElement):
    """<xs:element name="dashes" type="dashes"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='dashes', *args, **kwargs)
        NotImplementedError()


class Bracket(ComplexTypeBracket):
    _TAG = 'bracket'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Pedal(XMLElement):
    """<xs:element name="pedal" type="pedal"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='pedal', *args, **kwargs)
        NotImplementedError()


class Metronome(ComplexTypeMetronome):
    _TAG = 'metronome'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OctaveShift(XMLElement):
    """"<xs:element name="octave-shift" type="octave-shift"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='octave-shift', *args, **kwargs)
        NotImplementedError()


class HarpPedals(XMLElement):
    """"<xs:element name="harp-pedals" type="harp-pedals"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='harp-pedals', *args, **kwargs)
        NotImplementedError()


class Damp(EmptyPrintStyleAlignId):
    """
    The damp element specifies a harp damping mark.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='damp', *args, **kwargs)


class DampAll(EmptyPrintStyleAlignId):
    """
    The damp-all element specifies a harp damping mark for all strings.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='damp-all', *args, **kwargs)


class EyeGlasses(EmptyPrintStyleAlignId):
    """
    The eyeglasses element specifies the eyeglasses symbol, common in commercial music.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='eyeglasses', *args, **kwargs)


class StringMute(XMLElement):
    """"<xs:element name="string-mute" type="string-mute"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='string-mute', *args, **kwargs)
        NotImplementedError()


class Scordatura(XMLElement):
    """"<xs:element name="string-mute" type="string-mute"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='scordatura', *args, **kwargs)
        NotImplementedError()


class Image(XMLElement):
    """"<xs:element name="image" type="image"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='image', *args, **kwargs)
        NotImplementedError()


class PrincipalVoice(XMLElement):
    """"<xs:element name="principal-voice" type="principal-voice"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='principal-voice', *args, **kwargs)
        NotImplementedError()


class Percussion(XMLElement):
    """"<xs:element name="percussion" type="percussion" maxOccurs="unbounded"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='percussion', *args, **kwargs)
        NotImplementedError()


class StaffDivide(XMLElement):
    """"<xs:element name="staff-divide" type="staff-divide"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='staff-divide', *args, **kwargs)
        NotImplementedError()


class AccordionRegistration(XMLElement):
    """"<xs:element name="accordion-registration" type="accordion-registration"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='accordion-registration', *args, **kwargs)
        NotImplementedError()


class OtherDirection(XMLElement):
    """"<xs:element name="other-direction" type="other-direction"/>"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='other-direction', *args, **kwargs)
        NotImplementedError()


class ComplexTypeDirectionType(ComplexType, OptionalUniqueId):
    """Textual direction types may have more than 1 component due to multiple fonts. The dynamics element may also be
    used in the notations element. Attribute groups related to print suggestions apply to the individual direction-type,
    not to the overall direction."""

    _DTD = Choice(
        Element(Rehearsal, max_occurrence=None),
        Element(Segno, max_occurrence=None),
        Element(Coda, max_occurrence=None),
        Choice(
            Element(Words),
            # Element(Symbol),
            max_occurrence=None
        ),
        # Element(Words, max_occurrence=None),
        Element(Wedge),
        Element(Dynamics, max_occurrence=None),
        Element(Dashes),
        Element(Bracket),
        Element(Pedal),
        Element(Metronome),
        Element(OctaveShift),
        Element(HarpPedals),
        Element(Pedal),
        Element(DampAll),
        Element(EyeGlasses),
        Element(StringMute),
        Element(Scordatura),
        Element(Image),
        Element(PrincipalVoice),
        Element(Percussion, max_occurrence=None),
        Element(AccordionRegistration),
        Element(StaffDivide),
        Element(OtherDirection)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
