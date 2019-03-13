# from musicscore.musicxml.elements.xml_partwise import XMLMeasurePartwise, XMLPartPartwise, XMLScorePartwise
# from musicscore.musicxml.elements.xml_score_header import XMLPartList, XMLScorePart, XMLPartName
# from musicscore.musicxml.exceptions import ChildAlreadyExists
#
#
# class Partwise(XMLScorePartwise):
#     """"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def add_part(self, part=None):
#         if part is None:
#             part = PartPartwise()
#         if not isinstance(part, PartPartwise):
#             raise TypeError('part must be of type PartPartwise not{}'.format(type(part)))
#
#         try:
#             part_list = self.add_child(XMLPartList())
#         except ChildAlreadyExists:
#             pass
#
#         part_list.add_child(part.score_part)
#         self.add_child(part)
#         return part
#
#
# class PartPartwise(XMLPartPartwise):
#     _auto_index = 0
#     _ids = []
#
#     @staticmethod
#     def reset_ids():
#         PartPartwise._ids = []
#
#     def __init__(self, id=None, name=None, print_object='no', *args, **kwargs):
#         if id is None:
#             id = self.generate_id()
#         elif id in self._ids:
#             raise ValueError('part id {} already exists.'.format(id))
#         self._ids.append(id)
#         super().__init__(id=id, *args, **kwargs)
#         self.multiple = True
#         self._score_part = XMLScorePart(id=self.id)
#         self._score_part.part_name = XMLPartName(name=name, print_object=print_object)
#
#     def generate_id(self):
#         id = 'p' + str(self._auto_index + 1)
#         self._auto_index += 1
#
#         if id in self._ids:
#             id = self.generate_id()
#         return id
#
#     @property
#     def name(self):
#         return self._score_part.part_name.name
#
#     @name.setter
#     def name(self, value):
#         self._score_part.part_name.name = value
#
#     @property
#     def print_object(self):
#         return self._score_part.part_name.print_object
#
#     @print_object.setter
#     def print_object(self, value):
#         self._score_part.part_name.print_object = value
#
#     @property
#     def score_part(self):
#         return self._score_part
#
#     def add_measure(self, measure=None):
#         if measure is None:
#             measure = MeasurePartwise()
#         if not isinstance(measure, MeasurePartwise):
#             raise TypeError('measure must be of type MeasurePartwise not{}'.format(type(measure)))
#         self.add_child(measure)
#         measure.number = self.get_children().index(measure) + 1
#         return measure
#
#
# class MeasurePartwise(XMLMeasurePartwise):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(number=0, *args, **kwargs)
#         self.multiple = True
#
