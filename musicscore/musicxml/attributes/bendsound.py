from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract, TypeYesNo, TypeTrillBeats, TypePercent

class Accelerate(AttributeAbstract):
    def __init__(self, accelerate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('accelerate', accelerate, "TypeYesNo")
        TypeYesNo


class Beats(AttributeAbstract):
    def __init__(self, beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('beats', beats, "TypeTrillBeats")
        TypeTrillBeats


class FirstBeat(AttributeAbstract):
    def __init__(self, first_beat=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('first-beat', first_beat, "TypePercent")
        TypePercent


class LastBeat(AttributeAbstract):
    def __init__(self, last_beat=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('last-beat', last_beat, "TypePercent")
        TypePercent


class BendSound(Accelerate, Beats, FirstBeat, LastBeat):
    """
    The bend-sound type is used for bend and slide elements, and is similar to the trill-sound attribute group. Here
    the beats element refers to the number of discrete elements (like MIDI pitch bends) used to represent a continuous
    bend or slide. The first-beat indicates the percentage of the direction for starting a bend; the last-beat the
    percentage for ending it. The default choices are
    accelerate = "no"
    beats = "4"
    first-beat = "25"
    last-beat = "75"
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
