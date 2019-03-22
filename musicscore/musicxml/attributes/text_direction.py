from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Dir(AttributeAbstract):
    """"""

    def __init__(self, dir=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('dir', dir, "TextDirection")


class TextDirection(Dir):
    """
    The text-direction attribute is used to adjust and override the Unicode bidirectional text algorithm, similar to
    the W3C Internationalization Tag Set recommendation.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


"""
	<xs:attributeGroup name="text-direction">
		<xs:annotation>
			<xs:documentation></xs:documentation>
		</xs:annotation>
		<xs:attribute name="dir" type="text-direction"/>
	</xs:attributeGroup>
"""
