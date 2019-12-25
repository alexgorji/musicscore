from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeEnclosureShape


class Enclosure(AttributeAbstract):
    """
    The enclosure attribute group is used to specify the formatting of an enclosure around text or symbols.
    """

    def __init__(self, enclosure=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('enclosure', enclosure, "TypeEnclosureShape")
        TypeEnclosureShape
