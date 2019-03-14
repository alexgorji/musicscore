from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Width(AttributeAbstract):
    """"""
    # _ATTRIBUTES = ['width']

    def __init__(self, width=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('width', width, "Tenths")
