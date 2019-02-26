from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.basic_functions import is_empty
from musicscore.musicxml.attributes.print_object import PrintObject


class XMLPartName(XMLElement, PrintObject):
    _ATTRIBUTES = ['print-object']

    def __init__(self, name, print_object='no'):
        super().__init__(tag='part-name', print_object=print_object)
        self._name = None
        self.name = name

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


class XMLScorePart(XMLElement):
    _ATTRIBUTES = ('id')
    _CHILDREN_TYPES = [XMLPartName]

    def __init__(self, id, part_name='part'):
        super().__init__(tag='score-part')
        self._id = None
        self.id = id
        self._part_name = None
        self.part_name = part_name
        self.multiple = True

    @property
    def part_name(self):
        return self._part_name

    @part_name.setter
    def part_name(self, value):
        self._set_child(XMLPartName, 'part-name', value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
        self.set_attribute('id', self.id)


class XMLPartList(XMLElement):
    _CHILDREN_TYPES = [XMLScorePart]

    def __init__(self):
        super().__init__(tag='part-list')
