from musicxml.xmlelement.xmlelement import XMLPart

from musictree.musictree import MusicTree
from musictree.xmlwrapper import XMLWrapper


class Part(MusicTree, XMLWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLPart(*args, **kwargs)