# from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
# from musicscore.musicxml.elements.xml_music_data import XMLMusicData
# from musicscore.musicxml.elements.attributes import Attributes
#
#
# class PartTimewise(XMLPartAbstract):
#
#     _CHILDREN_TYPES = XMLPartAbstract._CHILDREN_TYPES
#     _CHILDREN_TYPES.extend([Attributes, XMLMusicData])
#
#     def __init__(self, id, *args, **kwargs):
#         super().__init__(id=id, *args, **kwargs)
#
#
# class MeasureTimewise(XMLMeasureAbstract):
#
#     _CHILDREN_TYPES = [PartTimewise]
#     _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)
#
#     def __init__(self, number, *args, **kwargs):
#         super().__init__(number=number, *args, **kwargs)
#         self.multiple = True
#
#
# class ScoreTimewise(XMLScoreAbstract):
#
#     _CHILDREN_TYPES = XMLScoreAbstract._CHILDREN_TYPES
#     _CHILDREN_TYPES.append(MeasureTimewise)
#
#     def __init__(self, *args, **kwargs):
#         XMLScoreAbstract.__init__(self, tag='score-timewise', *args, **kwargs)
#
#     def write(self, path):
#         xmlversion = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
#         doctype = '<!DOCTYPE score-timewise PUBLIC "-//Recordare//DTD MusicXML 3.0 Timewise//EN" "http://www.musicxml.org/dtds/timewise.dtd">\n'
#
#         path += '.xml'
#         output_file = open(path, 'w')
#         output_file.write(xmlversion)
#         output_file.write(doctype)
#         output_file.write(self.to_string())
#         output_file.close()
#         print('writing finished')
#
#
