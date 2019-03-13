# from musicscore.musicxml.elements.xml_element import XMLElement
# from musicscore.musicxml.elements.xml_score_header import XMLPartList
# from musicscore.musicxml.elements.attributes import Attributes
# from musicscore.musicxml.attributes.group_measure import Width
#
#
# class XMLMeasureAbstract(XMLElement, Width):
#     _ATTRIBUTES = ['number', 'width']
#     _CHILDREN_TYPES = [Attributes]
#
#     def __init__(self, number, *args, **kwargs):
#         super().__init__('measure', *args, **kwargs)
#         self._number = None
#         self.number = number
#
#     @property
#     def number(self):
#         return self._number
#
#     @number.setter
#     def number(self, value):
#         self._number = value
#         self.set_attribute('number', self.number)
#
#
# class XMLPartAbstract(XMLElement2):
#     _ATTRIBUTES = ['id']
#     _CHILDREN_TYPES = []
#
#     def __init__(self, id, *args, **kwargs):
#         super().__init__('part', *args, **kwargs)
#         self.multiple = True
#         self._id = None
#         self.id = id
#
#     @property
#     def id(self):
#         return self._id
#
#     @id.setter
#     def id(self, value):
#         self._id = value
#         self.set_attribute('id', self.id)
#
#
# class XMLScoreAbstract(XMLElement):
#     _CHILDREN_TYPES = [XMLPartList]
#     _CHILDREN_ORDERED = True
#
#     def __init__(self, tag, *args, **kwargs):
#         super().__init__(tag, *args, **kwargs)
