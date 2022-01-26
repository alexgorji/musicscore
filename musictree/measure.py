from musicxml.xmlelement.xmlelement import XMLMeasure, XMLAttributes

from musictree.musictree import MusicTree


class Measure(MusicTree):
    _ATTRIBUTES = {}

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLMeasure(*args, **kwargs)
        self.xml_object.xml_attributes = XMLAttributes()

    def check_divisions(self):
        pass

    def add_child(self, child):
        super().add_child(child)
        for note in child.notes:
            self.xml_object.add_child(note.xml_object)
            note.parent_measure = self
        child.update_notes_duration()