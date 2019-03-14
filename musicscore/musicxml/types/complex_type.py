from musicscore.dtd.dtd import Sequence, Choice, Group, Element
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.level_display import LevelDisplay
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.print_object import PrintObject
from musicscore.musicxml.attributes.print_style import PrintStyle
from musicscore.musicxml.elements.xml_element import XMLElement2
from musicscore.musicxml.types.simple_type import TypeStep, TypeAlter, TypeSemitones, TypeAccidentalValue, TypeMode, \
    TypeFifths, TypeOctave


class ComplexType(XMLElement2):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# TODO: add exception for attributes
class Empty(ComplexType, XMLElement2):
    """
    Empty is a type of XMLElement with no children, no text and no attributes
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

    def add_child(self, child):
        raise Exception('Empty cannot have children.')

    @XMLElement2.text.setter
    def text(self, value):
        if value is not None:
            raise Exception('Empty cannot have text.')


# class EmptyPlacement(Empty, PrintStyle, Placement):
# todo: Placement
class EmptyPlacement(Empty, PrintStyle):
    """
    The empty-placement type represents an empty element with print-style and placement attributes
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


class Reference(AttributeAbstract):
    def __init__(self, reference=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('reference', reference, 'YesNo')


class TypeLevel(ComplexType, Reference, LevelDisplay):
    _ATTRIBUTES = ['reference', 'parentheses', 'bracket', 'size']

    """The level type is used to specify editorial information for different MusicXML elements. If the reference
    attribute for the level element is yes, this indicates editorial information that is for display only and should
    not affect playback. For instance, a modern edition of older music may set reference="yes" on the attributes
    containing the music's original clef, key, and time signature. It is no by default
    	<xs:complexType name="level">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attribute name="reference" type="yes-no"/>
				<xs:attributeGroup ref="level-display"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Location(AttributeAbstract):
    """"""

    def __init__(self, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('location', location, 'CancelLocation')


class TypeCancel(ComplexType, TypeFifths, Location):
    """
    A cancel element indicates that the old key signature should be cancelled before the new one appears. This will
    always happen when changing to C major or A minor and need not be specified then. The cancel value matches the
    fifths value of the cancelled key signature (e.g., a cancel of -2 will provide an explicit cancellation for changing
    from B flat major to F major). The optional location attribute indicates where the cancellation appears relative to
    the new key signature.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Cancel(TypeCancel):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Fifths(XMLElement2, TypeFifths):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class Mode(XMLElement2, TypeMode):
    """"""

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


class KeyStep(XMLElement2, TypeStep):
    """
    Non-traditional key signatures can be represented using the Humdrum/Scot concept of a list of altered tones.
    The key-step element indicates the pitch step to be altered, represented using the same names as in the step
    element.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class KeyAlter(XMLElement2, TypeSemitones):
    """
    Non-traditional key signatures can be represented using the Humdrum/Scot concept of a list of altered tones.
    The key-step element indicates the pitch step to be altered, represented using the same names as in the step
    element.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class KeyAccidental(ComplexType, TypeAccidentalValue):
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


"""
The non-traditional-key group represents a single alteration within a non-traditional key signature. A sequence of 
these groups makes up a non-traditional key signature
"""
NonTraditionalKey = Sequence(
    Element(KeyStep),
    Element(KeyAlter),
    Element(KeyAccidental, min_occurrence=0)
)


class NumberAttribute(AttributeAbstract):
    """
    REQUIRED!
    """

    def __init__(self, number=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', number, 'PositiveInteger')


class CancelAttribute(AttributeAbstract):
    def __init__(self, cancel=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('cancel', cancel, 'YesNo')


class TypeKeyOctave(ComplexType, TypeOctave, NumberAttribute, CancelAttribute):
    """
    The key-octave element specifies in which octave an element of a key signature appears. The content specifies the
    octave value using the same values as the display-octave element. The number attribute is a positive integer that
    refers to the key signature element in left-to-right order. If the cancel attribute is set to yes, then this number
    refers to the canceling key signature specified by the cancel element in the parent key element. The cancel
    attribute cannot be set to yes if there is no corresponding cancel element within the parent key element. It is no
    by default
    """


class KeyOctave(TypeKeyOctave):

    def __init__(self, value, *args, **kwargs):
        super().__init__(value=value, *args, **kwargs)


class KeyNumberAttribute(AttributeAbstract):
    def __init__(self, cancel=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('number', cancel, 'StaffNumber')


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
                Group(TraditionalKey),
                Group(NonTraditionalKey, min_occurrence=0, max_occurrence=None)
            ),
            Element(KeyOctave, min_occurrence=0, max_occurrence=None)

        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
