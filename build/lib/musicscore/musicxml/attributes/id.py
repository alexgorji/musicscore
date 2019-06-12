from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Id(AttributeAbstract):
    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('id', id, "IDREF")
