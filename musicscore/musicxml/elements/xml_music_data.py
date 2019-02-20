from musicscore.musicxml.elements.xml_element import XMLElement


class XMLMusicData(XMLElement):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.multiple = True
