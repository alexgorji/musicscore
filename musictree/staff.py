from musicxml.xmlelement.xmlelement import XMLStaff

from musictree.exceptions import StaffHasNoParentError
from musictree.musictree import MusicTree
from musictree.voice import Voice
from musictree.xmlwrapper import XMLWrapper


class Staff(MusicTree, XMLWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLStaff(*args, **kwargs)

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

    def add_voice(self, voice=1):
        voice_object = self.get_voice(voice=voice)
        if voice_object is None:
            for _ in range(voice - len(self.get_children())):
                voice = self.add_child(Voice())
            return voice
        return voice_object

    def get_chords(self):
        return [ch for voice in self.get_children() for ch in voice.get_chords()]

    def get_voice(self, voice=1):
        for ch in self.get_children():
            if ch.value == voice:
                return ch
