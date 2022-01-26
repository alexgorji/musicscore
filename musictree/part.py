from musicxml.xmlelement.xmlelement import XMLPart

from musictree.musictree import MusicTree


class Part(MusicTree):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._xml_object = XMLPart(*args, **kwargs)