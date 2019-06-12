"""
	<xs:complexType name="slur">
		<xs:attribute name="type" type="start-stop-continue" use="required"/>
		<xs:attribute name="number" type="number-level" default="1"/>
		<xs:attributeGroup ref="line-type"/>
		<xs:attributeGroup ref="dashed-formatting"/>
		<xs:attributeGroup ref="position"/>
		<xs:attributeGroup ref="placement"/>
		<xs:attributeGroup ref="orientation"/>
		<xs:attributeGroup ref="bezier"/>
		<xs:attributeGroup ref="color"/>
		<xs:attributeGroup ref="optional-unique-id"/>
	</xs:complexType>
"""
from musicscore.musicxml.types.complextypes.complextype import ComplexType


class ComplexTypeSlur(ComplexType):
    """
    Slur types are empty. Most slurs are represented with two elements: one with a start type, and one with a stop type.
    Slurs can add more elements using a continue type. This is typically used to specify the formatting of cross-system
    slurs, or to specify the shape of very complex slurs.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        raise NotImplementedError()