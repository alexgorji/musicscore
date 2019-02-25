from musicscore.musicxml.elements.xml_element import XMLElement


class XMLMusicData(XMLElement):
    """The basic musical data that is either associated with a part or a measure, depending on whether partwise
    or timewise hierarchy is used.
    "(note | backup | forward | direction | attributes | harmony | figured-bass | print | sound | barline |  grouping |
    link | bookmark)*"
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self.multiple = True

class XMLBackup(XMLMusicData):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='backup', *args, **kwargs)


class XMLDirection(XMLMusicData):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='direction', *args, **kwargs)
