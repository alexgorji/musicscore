from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Rotation(AttributeAbstract):
    """"""

    def __init__(self, rotation=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('rotation', rotation, "TypeRotationDegrees")


class TextRotation(Rotation):
    """
    The rotation attribute is used to rotate text around the alignment point specified by the halign and valign
    attributes. Positive values are clockwise rotations, while negative values are counter-clockwise rotations.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
