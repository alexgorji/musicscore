"""
	<xs:complexType name="time-modification">
		<xs:sequence>
			<xs:element name="actual-notes" type="xs:nonNegativeInteger">
				<xs:annotation>
					<xs:documentation></xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="normal-notes" type="xs:nonNegativeInteger">
				<xs:annotation>
					<xs:documentation>.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:sequence minOccurs="0">
				<xs:element name="normal-type" type="note-type-value">
					<xs:annotation>
						<xs:documentation></xs:documentation>
					</xs:annotation>
				</xs:element>
				<xs:element name="normal-dot" type="empty" minOccurs="0" maxOccurs="unbounded">
					<xs:annotation>
						<xs:documentation></xs:documentation>
					</xs:annotation>
				</xs:element>
			</xs:sequence>
		</xs:sequence>
	</xs:complexType>
"""
from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.simple_type import NonNegativeInteger, TypeNoteTypeValue


class ActualNotes(XMLElement, NonNegativeInteger):
    """
    The actual-notes element describes how many notes are played in the time usually occupied by the number in the
    normal-notes element.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='actual-notes', value=value, *args, **kwargs)


class NormalNotes(XMLElement, NonNegativeInteger):
    """
    The normal-notes element describes how many notes are usually played in the time occupied by the number in the
    actual-notes element
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='normal-notes', value=value, *args, **kwargs)


class NormalType(XMLElement, TypeNoteTypeValue):
    """
    If the type associated with the number in the normal-notes element is different than the current note type (e.g.,
    a quarter note within an eighth note triplet), then the normal-notes type (e.g. eighth) is specified in the
    normal-type and normal-dot elements.
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='normal-type', value=value, *args, **kwargs)


class NormalDot(Empty):
    """
    The normal-dot element is used to specify dotted normal tuplet types..
    """

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='normal-dot', value=value, *args, **kwargs)


class ComplexTypeTimeModification(ComplexType):
    """
    Time modification indicates tuplets, double-note tremolos, and other durational changes. A time-modification element
    shows how the cumulative, sounding effect of tuplets and double-note tremolos compare to the written note type
    represented by the type and dot elements. Nested tuplets and other notations that use more detailed information need
    both the time-modification and tuplet elements to be represented accurately.
    """
    _DTD = Sequence(
        Element(ActualNotes),
        Element(NormalNotes),
        Sequence(
            Element(NormalType),
            Element(NormalDot, min_occurrence=0, max_occurrence=None),
            min_occurrence=0
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='time-modification', *args, **kwargs)
