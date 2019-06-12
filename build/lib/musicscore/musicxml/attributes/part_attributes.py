from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Id(AttributeAbstract):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('id', id, "IDREF")


class PartAttributes(Id):
    """
    In either partwise or timewise format, the part element has an id attribute that is an IDREF back to a score-part
    in the part-list.
    """

    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)
