from musicscore.musicxml.elements.xml_music_data import XMLMusicData
from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
from musicscore.musicxml.elements.xml_attributes import XMLAttributes


class XMLMeasurePartwise(XMLMeasureAbstract):

    # _CHILDREN_TYPES = [XMLMusicData]
    # _CHILDREN_TYPES.extend(XMLMeasureAbstract._CHILDREN_TYPES)
    _CHILDREN_TYPES = XMLMeasureAbstract._CHILDREN_TYPES
    _CHILDREN_TYPES.append(XMLMusicData)

    def __init__(self, number, *args, **kwargs):
        super().__init__(number=number, *args, **kwargs)


class XMLPartPartwise(XMLPartAbstract):

    _CHILDREN_TYPES = [XMLMeasurePartwise]
    _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)

    def __init__(self, id, *args, **kwargs):
        super().__init__(id=id, *args, **kwargs)


class XMLScorePartwise(XMLScoreAbstract):

    _CHILDREN_TYPES = XMLScoreAbstract._CHILDREN_TYPES
    _CHILDREN_TYPES.append(XMLPartPartwise)

    def __init__(self, *args, **kwargs):
        XMLScoreAbstract.__init__(self, tag='score-partwise', *args, **kwargs)

    def write(self, path):
        xmlversion = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        doctype = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">\n'

        path += '.xml'
        output_file = open(path, 'w')
        output_file.write(xmlversion)
        output_file.write(doctype)
        output_file.write(self.to_string())
        output_file.close()
        print('writing finished')


