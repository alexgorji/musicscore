from musicscore.musicxml.elements.xml_music_data import XMLMusicData
from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
from musicscore.musicxml.elements.xml_attributes import XMLAttributes


class XMLMeasurePartwise(XMLMeasureAbstract):

    _CHILDREN_TYPES = [XMLMusicData]
    _CHILDREN_TYPES.extend(XMLMeasureAbstract._CHILDREN_TYPES)

    def __init__(self, number, *args, **kwargs):
        super().__init__(number=number, *args, **kwargs)

    def add_music_data(self, child):
        if not isinstance(child, XMLMusicData):
            raise TypeError('child must be of type XMLMusicData not {}'.format(type(child)))
        return self.add_child(child)

    def add_xml_attribute(self, child):
        if not isinstance(self.get_children()[-1], XMLAttributes):
            xml_attributes = self.add_child(XMLAttributes())
        else:
            xml_attributes = self.get_children()[-1]

        return xml_attributes.add_child(child)


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


