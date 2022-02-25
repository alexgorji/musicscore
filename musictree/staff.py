from musicxml.xmlelement.xmlelement import XMLStaff

from musictree.clef import TrebleClef, Clef
from musictree.exceptions import StaffHasNoParentError
from musictree.core import MusicTree
from musictree.voice import Voice
from musictree.xmlwrapper import XMLWrapper


class Staff(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'clef', 'default_clef', 'number'}
    XMLClass = XMLStaff

    def __init__(self, number=None, clef=TrebleClef(), **kwargs):
        super().__init__()
        self._xml_object = self.XMLClass(value_=1, **kwargs)
        self._number = None
        self._clef = None
        self.clef = clef
        self.number = number

    @property
    def clef(self):
        return self._clef

    @clef.setter
    def clef(self, val):
        if val is not None and not isinstance(val, Clef):
            raise TypeError
        self._clef = val

    @property
    def number(self):
        if self._number is not None:
            return self.xml_object.value_
        else:
            return self._number

    @number.setter
    def number(self, val):
        self._number = val
        if val is None:
            self.xml_object.value_ = 1
        else:
            self.xml_object.value_ = val

    def add_child(self, child):
        self._check_child_to_be_added(child)

        if not self.up:
            raise StaffHasNoParentError('A child Voice can only be added to a Staff if staff has a Measure parent.')

        if child.number is not None and child.number != len(self.get_children()) + 1:
            raise ValueError(f'Voice number must be None or {len(self.get_children()) + 1}')
        if child.number is None:
            child.number = len(self.get_children()) + 1
        else:
            child.number = len(self.get_children()) + 1

        child._parent = self
        self._children.append(child)
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
