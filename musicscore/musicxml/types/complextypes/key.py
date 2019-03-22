from musicscore.dtd.dtd import Sequence, Choice, GroupReference, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.attributes.printstyle import PrintStyle
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.simple_type import TypeFifths, TypeMode, TypeStep, TypeSemitones, TypeAccidentalValue, \
    TypeOctave


class KeyNumberAttribute(AttributeAbstract):
    def __init__(self, cancel=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', cancel, 'StaffNumber')


class Location(AttributeAbstract):
    """"""

    def __init__(self, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('location', location, 'TypeCancelLocation')


class ComplexTypeCancel(ComplexType, TypeFifths, Location):
    """
    A cancel element indicates that the old key signature should be cancelled before the new one appears. This will
    always happen when changing to C major or A minor and need not be specified then. The cancel value matches the
    fifths value of the cancelled key signature (e.g., a cancel of -2 will provide an explicit cancellation for changing
    from B flat major to F major). The optional location attribute indicates where the cancellation appears relative to
    the new key signature.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Cancel(ComplexTypeCancel):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Fifths(XMLElement, TypeFifths):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Mode(XMLElement, TypeMode):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class KeyStep(XMLElement, TypeStep):
    """
    Non-traditional key signatures can be represented using the Humdrum/Scot concept of a list of altered tones.
    The key-step element indicates the pitch step to be altered, represented using the same names as in the step
    element.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class KeyAlter(XMLElement, TypeSemitones):
    """
    Non-traditional key signatures can be represented using the Humdrum/Scot concept of a list of altered tones.
    The key-step element indicates the pitch step to be altered, represented using the same names as in the step
    element.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class ComplexKeyAccidental(ComplexType, TypeAccidentalValue):
    """
    Non-traditional key signatures can be represented using the Humdrum/Scot concept of a list of altered tones.
    The key-accidental element indicates the accidental to be displayed in the key signature, represented in the same
    manner as the accidental element. It is used for disambiguating microtonal accidentals.
    <xs:simpleContent>
        <xs:extension base="accidental-value">
            <xs:attribute name="smufl" type="smufl-accidental-glyph-name"/>
        </xs:extension>
    </xs:simpleContent>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)
        raise NotImplementedError()


class Number(AttributeAbstract):
    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', number, 'PositiveInteger')


class CancelAttribute(AttributeAbstract):
    def __init__(self, cancel=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('cancel', cancel, 'TypeYesNo')


class ComplexTypeKeyOctave(ComplexType, TypeOctave, Number, CancelAttribute):
    """
    The key-octave element specifies in which octave an element of a key signature appears. The content specifies the
    octave value using the same values as the display-octave element. The number attribute is a positive integer that
    refers to the key signature element in left-to-right order. If the cancel attribute is set to yes, then this number
    refers to the canceling key signature specified by the cancel element in the parent key element. The cancel
    attribute cannot be set to yes if there is no corresponding cancel element within the parent key element. It is no
    by default
    """


class KeyOctave(ComplexTypeKeyOctave):

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


"""
The traditional-key group represents a traditional key signature using the cycle of fifths.
"""
TraditionalKey = Sequence(
    Element(Cancel, min_occurrence=0),
    Element(Fifths),
    Element(Mode, min_occurrence=0)

)
"""
The non-traditional-key group represents a single alteration within a non-traditional key signature. A sequence of 
these groups makes up a non-traditional key signature
"""
NonTraditionalKey = Sequence(
    Element(KeyStep),
    Element(KeyAlter),
    Element(ComplexKeyAccidental, min_occurrence=0)
)


class TypeKey(ComplexType, KeyNumberAttribute, PrintStyle, PrintObject,
              OptionalUniqueId):
    """
    The key type represents a key signature. Both traditional and non-traditional key signatures are supported.
    The optional number attribute refers to staff numbers. If absent, the key signature applies to all staves in the
    part. Key signatures appear at the start of each system unless the print-object attribute has been set to "no".
    """
    _DTD = (
        Sequence(
            Choice(
                GroupReference(TraditionalKey),
                GroupReference(NonTraditionalKey, min_occurrence=0, max_occurrence=None)
            ),
            Element(KeyOctave, min_occurrence=0, max_occurrence=None)

        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
