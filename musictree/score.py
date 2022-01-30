from musicxml.xmlelement.xmlelement import XMLScorePartwise, XMLPartList

from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper


class Score(MusicTree, XMLWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLScorePartwise(*args, **kwargs)
        self._xml_part_list = self._xml_object.add_child(XMLPartList())
