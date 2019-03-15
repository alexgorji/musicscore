from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Version(AttributeAbstract):
    """
    The color type indicates the color of an element. Color may be represented as hexadecimal RGB triples, as in HTML,
    or as hexadecimal ARGB tuples, with the A indicating alpha of transparency. An alpha value of 00 is totally
    transparent; FF is totally opaque. If RGB is used, the A value is assumed to be FF.  For instance, the RGB value
    "#800080" represents purple. An ARGB value of "#40800080" would be a transparent purple.  As in SVG 1.1, colors are
    defined in terms of the sRGB color space (IEC 61966).
    """

    def __init__(self, version, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('version', version, 'Token')


class DocumentAttributes(Version):
    def __init__(self, version='1.0', *args, **kwargs):
        super().__init__(version=version, *args, **kwargs)
