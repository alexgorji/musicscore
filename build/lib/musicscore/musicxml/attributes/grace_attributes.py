from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class StealTimePrevious(AttributeAbstract):

    def __init__(self, steal_time_previous=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('steal-time-previous', steal_time_previous, 'Percent')


class StealTimeFollowing(AttributeAbstract):

    def __init__(self, steal_time_following=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('steal-time-following', steal_time_following, 'TypePercent')


class MakeTime(AttributeAbstract):

    def __init__(self, make_time=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('make-time', make_time, 'TypeDivisions')


class Slash(AttributeAbstract):

    def __init__(self, slash=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('slash', slash, 'TypeYesNo')
