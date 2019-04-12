from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Orientation(AttributeAbstract):
    """
    The orientation attribute indicates whether slurs and ties are overhand (tips down) or underhand (tips up). This is
     distinct from the placement attribute used by any notation type.
    """

    def __init__(self, orientation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('orientation', orientation, "OverUnder")


"""
	<xs:attributeGroup name="orientation">
		<xs:annotation>
			<xs:documentation></xs:documentation>
		</xs:annotation>
		<xs:attribute name="orientation" type="over-under"/>
	</xs:attributeGroup>
"""