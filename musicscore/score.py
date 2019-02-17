from py_musicxml.elements.xml_element import XMLElement

class Music(object):
    """"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._element = None

    @property
    def element(self):
        return self._element
        
    @element.setter
    def element(self, value):
        if not isinstance(value, XMLElement):
            raise TypeError('element.value must be of type XMLElement not{}'.format(type(value)))
        self._element = value


class Score(Music):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._measures = []
        
    @property
    def measures(self):
        return self._measures
        
    @measures.setter
    def measures(self, value):
        if not isinstance(value, list):
            raise TypeError('measures.value must be of type list not{}'.format(type(value)))
        for element in value:
            if not isinstance(element, Measure):
                raise TypeError('measures.value.element  must be of type Measure not{}'.format(type(element)))
        self._measures = value


class Part(Music):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Measure(Music):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

