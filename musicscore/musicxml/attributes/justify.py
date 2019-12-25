from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeLeftCenterRight


class Justify(AttributeAbstract):
    """
    The justify attribute is used to indicate left, center, or right justification. The default value varies for
    different elements. For elements where the justify attribute is present but the halign attribute is not, the justify
    attribute indicates horizontal alignment as well as justification.
    """

    def __init__(self, justify=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('justify', justify, "TypeLeftCenterRight")
        TypeLeftCenterRight
