from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLPartList

from musictree.musictree import MusicTree
from musictree.quarterduration import QuarterDuration
from musictree.xmlwrapper import XMLWrapper


class Score(MusicTree, XMLWrapper):
    _ATTRIBUTES = {'version'}

    def __init__(self, version='4.0', *args, **kwargs):
        super().__init__()
        self._xml_object = XMLScorePartwise(*args, **kwargs)
        self._xml_object.add_child(XMLPartList())
        self._version = None
        self.version = version
        self._possible_subdivisions = {QuarterDuration(1, 4): [2, 3], QuarterDuration(1, 2): [2, 3, 4, 5], QuarterDuration(1): [2, 3, 4,
                                                                                                                                5, 6, 7, 8]}

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

    def export_xml(self, path):
        with open(path, '+w') as f:
            f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE score-partwise PUBLIC
    "-//Recordare//DTD MusicXML 4.0 Partwise//EN"
    "http://www.musicxml.org/dtds/partwise.dtd">
""")
            f.write(self.to_string())

    def update(self):
        for p in self.get_children():
            p.update()
