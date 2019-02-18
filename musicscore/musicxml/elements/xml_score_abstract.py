from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.elements.xml_score_header import XMLPartList
from musicscore.musicxml.elements.xml_attributes import XMLAttributes


class XMLMeasureAbstract(XMLElement):

    _CHILDREN_TYPES = [XMLAttributes]

    def __init__(self, number, *args, **kwargs):
        super().__init__('measure', *args, **kwargs)
        self._number = None
        self.number = number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        self.set_attribute('number', self.number)


class XMLPartAbstract(XMLElement):

    _CHILDREN_TYPES = []

    def __init__(self, id, *args, **kwargs):
        super().__init__('part', *args, **kwargs)
        self._id = None
        self.id = id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self.set_attribute('id', self.id)


class XMLScoreAbstract(XMLElement):

    _CHILDREN_TYPES = [XMLPartList]

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag, *args, **kwargs)
        self._part_list = XMLPartList()
        self.add_child(self._part_list)

    def add_score_part(self, value):
        self._part_list.add_score_part(value)

