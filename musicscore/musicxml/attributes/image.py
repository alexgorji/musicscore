'''
	<xs:attributeGroup name="image-attributes">
		<xs:annotation>
			<xs:documentation></xs:documentation>
		</xs:annotation>
		<xs:attributeGroup ref="position"/>
		<xs:attributeGroup ref="halign"/>
		<xs:attributeGroup ref="valign-image"/>
	</xs:attributeGroup>
'''
from musicscore.musicxml.attributes.align import Halign, ValignImage
from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract
from musicscore.musicxml.attributes.position import Position
from musicscore.musicxml.types.simple_type import Token


class Source(AttributeAbstract):
    def __init__(self, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('source', source, "AnyURI")


class Height(AttributeAbstract):
    def __init__(self, height=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('height', height, "Tenths")


class Width(AttributeAbstract):
    def __init__(self, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('width', width, "Tenths")


class ImageAttributes(Source, Height, Width, Position, Halign, ValignImage):
    """
    The image-attributes group is used to include graphical images in a score. The required source attribute is the URL
    for the image file. The required type attribute is the MIME type for the image file format. Typical choices include
    application/postscript, image/gif, image/jpeg, image/png, and image/tiff. The optional height and width attributes
    are used to size and scale an image. The image should be scaled independently in X and Y if both height and width
    are specified. If only one attribute is specified, the image should be scaled proportionally to fit in the
    specified dimension.
    """

    def __init__(self, _type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = _type

    @property
    def type(self):
        return self.get_attribute('type')

    @type.setter
    def type(self, value):
        if value is None:
            self.remove_attribute('type')
        else:
            Token(value)
            self._ATTRIBUTES.insert(0, 'type')
            self.set_attribute('type', value)
