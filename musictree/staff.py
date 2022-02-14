from musicxml.xmlelement.xmlelement import XMLStaff

from musictree.clef import TrebleClef, Clef
from musictree.exceptions import StaffHasNoParentError
from musictree.musictree import MusicTree
from musictree.voice import Voice
from musictree.xmlwrapper import XMLWrapper


class Staff(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'clef', 'default_clef'}

    def __init__(self, clef=None, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLStaff(*args, **kwargs)
        self._clef = None
        self._default_clef = TrebleClef()
        self.clef = clef

    @property
    def default_clef(self):
        return self._default_clef

    @default_clef.setter
    def default_clef(self, val):
        if not isinstance(val, Clef):
            raise TypeError
        self._default_clef = val

    @property
    def clef(self):
        if self._clef is None:
            return self._default_clef
        return self._clef

    @clef.setter
    def clef(self, val):
        if val is not None and not isinstance(val, Clef):
            raise TypeError
        self._clef = val

    def add_child(self, child):
        if not self.up:
            raise StaffHasNoParentError('A child Voice can only be added to a Staff if staff has a Measure parent.')

        if child.value is not None and child.value != len(self.get_children()) + 1:
            raise ValueError(f'Voice number must be None or {len(self.get_children()) + 1}')
        if child.value is None:
            child.value = len(self.get_children()) + 1
        else:
            child.value = len(self.get_children()) + 1

        super().add_child(child)
        child.update_beats()

        return child

    def add_voice(self, voice_number=None):
        if voice_number is None:
            voice_number = len(self.get_children()) + 1
            # voice_number = 1
        voice_object = self.get_voice(voice_number=voice_number)
        if voice_object is None:
            for _ in range(voice_number - len(self.get_children())):
                voice_object = self.add_child(Voice())
            return voice_object
        return voice_object

    def get_chords(self):
        return [ch for voice in self.get_children() for ch in voice.get_chords()]

    def get_voice(self, voice_number=1):
        for ch in self.get_children():
            if ch.value == voice_number:
                return ch

    def get_previous_staff(self):
        if self.up and self.up.previous:
            my_index = self.up.get_children().index(self)
            try:
                return self.up.previous.get_children()[my_index]
            except IndexError:
                return None
        return None

    def get_last_steps_with_accidentals(self):
        output = set()
        for v in self.get_children():
            if v.get_chords():
                last_chord = v.get_chords()[-1]
                if not last_chord.is_rest:
                    for m in last_chord.midis:
                        if m.accidental.sign != 'natural':
                            step = m.accidental.get_pitch_parameters()[0]
                            if step not in output:
                                output.add(step)
        return output
