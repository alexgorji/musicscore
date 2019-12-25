from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeLineType


class LineType(AttributeAbstract):
    """
    The line-type attribute distinguishes between solid, dashed, dotted, and wavy lines.
    """

    def __init__(self, line_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-type', line_type, "TypeLineType")
        TypeLineType