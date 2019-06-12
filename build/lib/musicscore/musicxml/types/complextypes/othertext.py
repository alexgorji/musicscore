'''
	<xs:complexType name="other-text">
		<xs:annotation>
			<xs:documentation></xs:documentation>
		</xs:annotation>
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attributeGroup ref="smufl"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
'''
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeOtherText(ComplexType):
    """
    The other-text type represents a text element with a smufl attribute group. This type is used by MusicXML direction
    extension elements to allow specification of specific SMuFL glyphs without needed to add every glyph as a MusicXML
    element.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        NotImplementedError()
