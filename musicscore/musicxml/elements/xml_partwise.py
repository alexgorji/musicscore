from musicscore.musicxml.elements.xml_music_data import XMLMusicData
from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
from musicscore.musicxml.elements.xml_attributes import XMLAttributes


class XMLMeasurePartwise(XMLMeasureAbstract):

    _CHILDREN_TYPES = [XMLMusicData]
    _CHILDREN_TYPES.extend(XMLMeasureAbstract._CHILDREN_TYPES)

    def __init__(self, number):
        super().__init__(number=number)

    def add_music_data(self, child):
        if not isinstance(child, XMLMusicData):
            raise TypeError('child must be of type XMLMusicData not {}'.format(type(child)))
        return self.add_child(child)

    def add_attribute(self, child):
        if not isinstance(self.get_children()[-1], XMLAttributes):
            attributes = self.add_child(XMLAttributes())
        else:
            attributes = self.get_children()[-1]

        return attributes.add_child(child)


class XMLPartPartwise(XMLPartAbstract):

    _CHILDREN_TYPES = [XMLMeasurePartwise]
    _CHILDREN_TYPES.extend(XMLPartAbstract._CHILDREN_TYPES)

    def __init__(self, id):
        super().__init__(id=id)


class XMLScorePartwise(XMLScoreAbstract):

    _CHILDREN_TYPES = [XMLPartPartwise]
    _CHILDREN_TYPES.extend(XMLScoreAbstract._CHILDREN_TYPES)

    def __init__(self):
        XMLScoreAbstract.__init__(self, tag='score-partwise')


