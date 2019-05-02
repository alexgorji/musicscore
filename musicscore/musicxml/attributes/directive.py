from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Directive(AttributeAbstract):
    """
    The directive attribute changes the default-x position of a direction. It indicates that the left-hand side of
    the direction is aligned with the left-hand side of the time signature. If no time signature is present, it is
    aligned with the left-hand side of the first music notational element in the measure. If a default-x, justify,
    or halign attribute is present, it overrides the directive attribute.
    """

    def __init__(self, directive=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('directive', directive, 'TypeYesNo')
