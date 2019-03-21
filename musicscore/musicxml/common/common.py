from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.types.complex_type import ComplexType
from musicscore.musicxml.types.simple_type import String


class FormattedText(ComplexType, String, TextFormatting):
    """
    The formatted-text type represents a text element with text-formatting attributes.
    """

    """
    	<xs:complexType name="formatted-text">
		<xs:simpleContent>
			<xs:extension base="xs:string">
				<xs:attributeGroup ref="text-formatting"/>
			</xs:extension>
		</xs:simpleContent>
	</xs:complexType>
    """

"""
The footnote element specifies editorial information that appears in footnotes in the printed score. It is defined 
within a group due to its multiple uses within the MusicXML schema.
"""

class FootNote(FormattedText):
    pass


"""
The editorial group specifies editorial information for a musical element.
"""
Editorial = Sequence(
    Element(FootNote, min_occurrence=0),
    Element(Level, min_occurrence=0)
)
