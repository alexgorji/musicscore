from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class LineLength(AttributeAbstract):
    """
    The line-length attribute distinguishes between different line lengths for doit, falloff, plop, and scoop
    articulations.
    """

    def __init__(self, line_length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('line-length', line_length, "TypeLineLength")