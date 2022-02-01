from musicxml.xmlelement.xmlelement import XMLMeasure, XMLAttributes

from musictree.musictree import MusicTree
from musictree.staff import Staff
from musictree.time import Time
from musictree.voice import Voice
from musictree.xmlwrapper import XMLWrapper


class Measure(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'number', 'time', 'chords'}

    def __init__(self, number, time=None, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLMeasure(*args, **kwargs)
        # self.xml_object.xml_attributes = XMLAttributes()
        self.number = number
        self._time = None
        self.time = time
        self._chords = []

    @property
    def chords(self):
        return self._chords

    @property
    def number(self):
        return int(self.xml_object.number)

    @number.setter
    def number(self, val):
        self.xml_object.number = str(val)

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, val):
        if val is not None and not isinstance(val, Time):
            raise TypeError()
        if val is None:
            val = Time()
        self._time = val
        self._time.parent_measure = self
        self.update_voice_beats()

    def update_voice_beats(self):
        for staff in self.get_children():
            for voice in staff.get_children():
                voice.update_beats()

    def add_child(self, child):
        if child.value is not None and child.value != len(self.get_children()) + 1:
            raise ValueError(f'Staff number must be None or {len(self.get_children()) + 1}')
        if child.value is None:
            if not self.get_children():
                pass
            elif len(self.get_children()) == 1:
                self.get_children()[0].value = 1
                child.value = len(self.get_children()) + 1
            else:
                child.value = len(self.get_children()) + 1

        return super().add_child(child)

    def check_divisions(self):
        pass

    def add_chord(self, chord, staff=1, voice=1):
        for x in range(staff - len(self.get_children())):
            self.add_child(Staff())
        staff = self.get_children()[staff - 1]
        for x in range(voice - len(staff.get_children())):
            staff.add_child(Voice())
        voice = staff.get_children()[voice - 1]
        return voice.add_chord(chord)
