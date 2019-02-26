from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class AttributeExample(AttributeAbstract):
    """"""

    def __init__(self, attribute_example=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('attribute-example', attribute_example, "ExampleType")
