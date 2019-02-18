from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLPartPartwise
from musicscore.musicxml.elements.xml_timewise import XMLScoreTimewise, XMLMeasureTimewise


class Score(object):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._partwise = None
        self._timewise = None

    @property
    def partwise(self):
        return self._partwise

    @partwise.setter
    def partwise(self, value):
        if not isinstance(value, Partwise):
            raise TypeError('partwise.value must be of type Partwise not{}'.format(type(value)))
        self._partwise = value

    @property
    def timewise(self):
        return self._timewise

    @timewise.setter
    def timewise(self, value):
        if not isinstance(value, Timewise):
            raise TypeError('Timewise.value must be of type Timewise not{}'.format(type(value)))
        self._timewise = value

    def add_part(self, part=None):
        if part is None:
            part = Part()
        self.partwise.parts.append(part)


class Part(XMLPartPartwise):
    _auto_index = 0
    _ids = [].copy()

    def generate_id(self):
        id = 'p' + str(self._auto_index + 1)
        self._auto_index += 1

        if id in self._ids:
            id = self.generate_id()

        return id

    def __init__(self, id=None, *args, **kwargs):
        if id is None:
            id = self.generate_id()
        elif id in self._ids:
            raise ValueError('part id {} already exists.'.format(id))
        self._ids.append(id)
        super().__init__(id=id, *args, **kwargs)


class Partwise(XMLScorePartwise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = [].copy()

    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, value):
        if not isinstance(value, list):
            raise TypeError('parts.value must be of type list not{}'.format(type(value)))
        for element in value:
            if not isinstance(element, XMLPartPartwise):
                raise TypeError('parts.value.element  must be of type XMLPartTimewise not{}'.format(type(element)))
        self._parts = value


class Timewise(XMLScoreTimewise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._measures = [].copy()

    @property
    def measures(self):
        return self._measures

    @measures.setter
    def measures(self, value):
        if not isinstance(value, list):
            raise TypeError('measures.value must be of type list not{}'.format(type(value)))
        for element in value:
            if not isinstance(element, XMLMeasureTimewise):
                raise TypeError(
                    'measures.value.element  must be of type XMLMeasureTimewise not{}'.format(type(element)))
        self._measures = value
