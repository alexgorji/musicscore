from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class Placement(AttributeAbstract):
    def __init__(self, placement=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('placement', placement, 'TypeAboveBelow')
