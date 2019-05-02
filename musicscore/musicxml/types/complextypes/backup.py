'''
	<xs:complexType name="backup">
		<xs:annotation>
			<xs:documentation></xs:documentation>
		</xs:annotation>
		<xs:sequence>
			<xs:group ref="duration"/>
			<xs:group ref="editorial"/>
		</xs:sequence>
	</xs:complexType>
'''
from musicscore.dtd.dtd import Sequence, GroupReference, Element
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.elements.note import Duration
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeBackup(ComplexType):
    """
    The backup and forward elements are required to coordinate multiple voices in one part, including music on multiple
    staves. The backup type is generally used to move between voices and staves. Thus the backup element does not
    include voice or staff elements. Duration values should always be positive, and should not cross measure boundaries
    or mid-measure changes in the divisions value.
    """
    _DTD = Sequence(
        Element(Duration),
        GroupReference(Editorial)
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
