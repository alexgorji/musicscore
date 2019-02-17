from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
from musicscore.musicxml.elements.xml_music_data import XMLMusicData
from musicscore.musicxml.elements.xml_attributes import XMLAttributes


class XMLPartTimewise(XMLPartAbstract):

    _CHILDREN_TYPES = [XMLMusicData]
    _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)

    def __init__(self, id):
        super().__init__(id=id)

    def add_music_data(self, child):
        if not isinstance(child, XMLMusicData):
            raise TypeError('child must be of type XMLMusicData not {}'.format(type(child)))
        return self.add_child(child)


class XMLMeasureTimewise(XMLMeasureAbstract):

    _CHILDREN_TYPES = [XMLPartTimewise]
    _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)

    def __init__(self, number):
        super().__init__(number=number)

    def add_xml_attribute(self, child):
        if not isinstance(self.get_children()[-1], XMLAttributes):
            xml_attributes = self.add_child(XMLAttributes())
        else:
            xml_attributes = self.get_children()[-1]

        return xml_attributes.add_child(child)


class XMLScoreTimewise(XMLScoreAbstract):

    _CHILDREN_TYPES = [XMLMeasureTimewise]
    _CHILDREN_TYPES.extend(XMLScoreAbstract._CHILDREN_TYPES)

    def __init__(self):
        XMLScoreAbstract.__init__(self, tag='score-timewise')




