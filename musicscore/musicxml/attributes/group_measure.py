from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Width(AttributeAbstract):
    """"""

    def __init__(self, tag, width=None, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('width', width, "Tenths")
