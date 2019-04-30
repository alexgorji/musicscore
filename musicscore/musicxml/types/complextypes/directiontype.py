from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.formattedtextid import ComplexTypeFormattedTextId


class Rehearsal(ComplexTypeFormattedTextId):
    """The rehearsal type specifies a rehearsal mark. Language is Italian ("it") by default. Enclosure is square by
    default. Left justification is assumed if not specified.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='rehearsal', *args, **kwargs)


class ComplexTypeDirectionType(ComplexType):
    """Textual direction types may have more than 1 component due to multiple fonts. The dynamics element may also be
    used in the notations element. Attribute groups related to print suggestions apply to the individual direction-type,
    not to the overall direction."""

    _DTD = Choice(
        Element(Rehearsal, max_occurrence=None),
        Element(Segno, max_occurrence=None)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)


'''
	<xs:complexType name="direction-type">
		<xs:choice>
			<xs:element name="segno" type="segno" maxOccurs="unbounded"/>
			<xs:element name="coda" type="coda" maxOccurs="unbounded"/>
			<xs:choice maxOccurs="unbounded">
				<xs:element name="words" type="formatted-text-id">
					<xs:annotation>
						<xs:documentation>The words element specifies a standard text direction. Left justification is assumed if not specified. Language is Italian ("it") by default. Enclosure is none by default.</xs:documentation>
					</xs:annotation>
				</xs:element>
				<xs:element name="symbol" type="formatted-symbol-id">
					<xs:annotation>
						<xs:documentation>The symbol element specifies a musical symbol using a canonical SMuFL glyph name. It is used when an occasional musical symbol is interspersed into text. It should not be used in place of semantic markup, such as metronome marks that mix text and symbols. Left justification is assumed if not specified. Enclosure is none by default.</xs:documentation>
					</xs:annotation>
				</xs:element>
			</xs:choice>
			<xs:element name="wedge" type="wedge"/>
			<xs:element name="dynamics" type="dynamics" maxOccurs="unbounded"/>
			<xs:element name="dashes" type="dashes"/>
			<xs:element name="bracket" type="bracket"/>
			<xs:element name="pedal" type="pedal"/>
			<xs:element name="metronome" type="metronome"/>
			<xs:element name="octave-shift" type="octave-shift"/>
			<xs:element name="harp-pedals" type="harp-pedals"/>
			<xs:element name="damp" type="empty-print-style-align-id">
				<xs:annotation>
					<xs:documentation>The damp element specifies a harp damping mark.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="damp-all" type="empty-print-style-align-id">
				<xs:annotation>
					<xs:documentation>The damp-all element specifies a harp damping mark for all strings.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="eyeglasses" type="empty-print-style-align-id">
				<xs:annotation>
					<xs:documentation>The eyeglasses element specifies the eyeglasses symbol, common in commercial music.</xs:documentation>
				</xs:annotation>
			</xs:element>
			<xs:element name="string-mute" type="string-mute"/>
			<xs:element name="scordatura" type="scordatura"/>
			<xs:element name="image" type="image"/>
			<xs:element name="principal-voice" type="principal-voice"/>
			<xs:element name="percussion" type="percussion" maxOccurs="unbounded"/>
			<xs:element name="accordion-registration" type="accordion-registration"/>
			<xs:element name="staff-divide" type="staff-divide"/>
			<xs:element name="other-direction" type="other-direction"/>
		</xs:choice>
		<xs:attributeGroup ref="optional-unique-id"/>
	</xs:complexType>
'''
