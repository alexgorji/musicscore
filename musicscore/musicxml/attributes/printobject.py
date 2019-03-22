from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class PrintObject(AttributeAbstract):
    """"""

    def __init__(self, print_object=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('print-object', print_object, "TypeYesNo")
