from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.simple_type import YesNo
from musicscore.basic_functions import is_empty


class XMLPartName(XMLElement):
    def __init__(self, name, print_object='no'):
        super().__init__(tag='part-name')
        self._name = None
        self.name = name
        self.print_object = print_object

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        if self.name is None or is_empty(self.name):
            self.text = 'none'
        else:
            self.text = self.name

    @property
    def print_object(self):
        return self.get_attribute('print-object')

    @print_object.setter
    def print_object(self, value):
        YesNo(value)
        self.set_attribute('print-object', value)


class XMLScorePart(XMLElement):
    _CHILDREN_TYPES = [XMLPartName]

    def __init__(self, id, part_name='part'):
        super().__init__(tag='score-part')
        self.set_attribute('id', id)
        self._part_name = None
        self.part_name = part_name
        self.multiple = True

    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        self._set_child(XMLPartName, 'part-name', value)


class XMLPartList(XMLElement):
    _CHILDREN_TYPES = [XMLScorePart]

    def __init__(self):
        super().__init__(tag='part-list')
