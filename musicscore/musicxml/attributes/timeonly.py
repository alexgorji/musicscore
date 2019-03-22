from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class TimeOnly(AttributeAbstract):
    def __init__(self, time_only=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('time-only', time_only, 'TypeTimeOnly')