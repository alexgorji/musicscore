from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class LineShape(AttributeAbstract):
    """
	The line-shape attribute distinguishes between straight and curved lines.
    """

    def __init__(self, line_shape=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-shape', line_shape, "TypeLineShape")
