from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLPartList, XMLScorePart

from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper


class Score(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'version'}

    def __init__(self, version='4.0', *args, **kwargs):
        super().__init__()
        self._xml_object = XMLScorePartwise(*args, **kwargs)
        self._xml_object.add_child(XMLPartList())
        self._version = None
        self.version = version

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = str(val)
        self.xml_object.version = self.version

    def add_child(self, child):
        super().add_child(child)
        self.xml_object.add_child(child.xml_object)
        self.xml_part_list.xml_score_part = child.score_part.xml_object
        return child

    def get_chords(self):
        return [ch for part in self.get_children() for measure in part.get_children() for staff in measure.get_children() for voice in
                staff.get_children() for beat in voice.get_children() for ch in beat.get_children()]

    def update_xml_notes(self):
        for measure in [m for p in self.get_children() for m in p.get_children()]:
            measure.update_xml_notes()
