from musicscore.musicxml.attributes.attribute_abstract import AttributeAbstract


class StartNote(AttributeAbstract):
    def __init__(self, start_note=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('start-note', start_note, "TypeStartNote")


class TrillStep(AttributeAbstract):
    def __init__(self, start_note=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('trill-step', start_note, "TypeTrillStep")


class TwoNoteTurn(AttributeAbstract):
    def __init__(self, two_note_turn=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('two-note-turn', two_note_turn, "TypeTwoNoteTurn")


class Accelerate(AttributeAbstract):
    def __init__(self, accelerate=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('accelerate', accelerate, "TypeYesNo")


class SecondBeat(AttributeAbstract):
    def __init__(self, second_beat=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('second-beat', second_beat, "TypePercent")


class LastBeat(AttributeAbstract):
    def __init__(self, last_beat=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('last-beat', last_beat, "TypePercent")


class Beats(AttributeAbstract):
    def __init__(self, beats=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_attribute('beats', beats, "TypeTrillBeats")


class TrillSound(StartNote, TrillStep, TwoNoteTurn, Accelerate, Beats, SecondBeat, LastBeat):
    """
    The trill-sound attribute group includes attributes used to guide the sound of trills, mordents, turns, shakes, and
    wavy lines, based on MuseData sound suggestions. The default choices are:

                start-note = "upper"
                trill-step = "whole"
                two-note-turn = "none"
                accelerate = "no"
                beats = "4".

                Second-beat and last-beat are percentages for landing on the indicated beat, with defaults of 25 and 75
                respectively.

                For mordent and inverted-mordent elements, the defaults are different:

                The default start-note is "main", not "upper".
                The default for beats is "3", not "4".
                The default for second-beat is "12", not "25".
                The default for last-beat is "24", not "75".
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
