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
