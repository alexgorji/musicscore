from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class PrintObject(AttributeAbstract):
    """"""

    def __init__(self, tag, print_object='yes', *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.generate_attribute('print-object', print_object, "YesNo")
