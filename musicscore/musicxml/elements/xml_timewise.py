from musicscore.musicxml.elements.xml_score_abstract import XMLMeasureAbstract, XMLPartAbstract, XMLScoreAbstract
from musicscore.musicxml.elements.xml_music_data import XMLMusicData


class XMLPartTimewise(XMLPartAbstract):
    def __init__(self, id):
        super().__init__(id=id)

    def add_child(self, child):
        if not isinstance(child, XMLMusicData):
            raise TypeError('child must be of type XMLMusicData not {}'.format(type(child)))
        self._children.append(child)


class XMLMeasureTimewise(XMLMeasureAbstract):
    def __init__(self, number):
        super().__init__(number=number)

    def add_part(self, part):
        if not isinstance(part, XMLPartTimewise):
            raise TypeError('child must be of type XMLPartTimewise not {}'.format(type(child)))
        self._children.append(part)


class XMLScoreTimewise(XMLScoreAbstract):
    def __init__(self):
        XMLScoreAbstract.__init__(self, tag='score-partwise')

    def add_part(self, measure):
        if not isinstance(measure, XMLMeasureTimewise):
            raise TypeError('measure must be of type XMLMeasureTimewise and not {}'.format(type(part)))
        return self.add_child(measure)



