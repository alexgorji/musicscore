from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLPartPartwise
from musicscore.musicxml.elements.xml_timewise import XMLScoreTimewise, XMLMeasureTimewise
from musicscore.musicxml.elements.xml_score_header import XMLScorePart, XMLPartName


class Measure(XMLMeasureTimewise):
    _auto_index = 0

    def generate_number(self):
        number = self._auto_index + 1
        self._auto_index += 1
        return number

    def __init__(self, *args, **kwargs):
        super().__init__(number=self.generate_number(), *args, **kwargs)


class Part(XMLPartPartwise):
    _auto_index = 0
    _ids = [].copy()

    @staticmethod
    def reset_ids():
        _ids = [].copy()

    def __init__(self, id=None, name=None, *args, **kwargs):
        if id is None:
            id = self.generate_id()
        elif id in self._ids:
            raise ValueError('part id {} already exists.'.format(id))
        self._ids.append(id)
        super().__init__(id=id, *args, **kwargs)
        self._score_part = XMLScorePart(id=self.id)
        self._score_part.part_name = XMLPartName(name)

    def generate_id(self):
        id = 'p' + str(self._auto_index + 1)
        self._auto_index += 1

        if id in self._ids:
            id = self.generate_id()
        return id

    @property
    def name(self):
        return self._score_part.part_name.name

    @name.setter
    def name(self, value):
        self._score_part.part_name.name = value

    @property
    def print_object(self):
        return self._score_part.part_name.print_object

    @print_object.setter
    def print_object(self, value):
        self._score_part.part_name.print_object = value


class Score(object):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._partwise = Partwise()
        self._timewise = Timewise()

    @property
    def partwise(self):
        return self._partwise

    @partwise.setter
    def partwise(self, value):
        if not isinstance(value, Partwise):
            raise TypeError('partwise.value must be of type Partwise not{}'.format(type(value)))
        self._partwise = value
        self.partwise.score = self

    @property
    def timewise(self):
        return self._timewise

    @timewise.setter
    def timewise(self, value):
        if not isinstance(value, Timewise):
            raise TypeError('Timewise.value must be of type Timewise not{}'.format(type(value)))
        self._timewise = value
        self.timewise.score = self

    def add_part(self, part=None):
        if part is None:
            part = Part()
        self.partwise.parts.append(part)
        self.partwise.add_score_part(part._score_part)
        self.timewise.add_score_part(part._score_part)

    def add_measure(self, measure=None):
        if measure is None:
            measure = Measure()
        self.measurewise.measures.append(measure)


class Partwise(XMLScorePartwise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parts = [].copy()
        self._score = None

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

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, Score):
            raise TypeError('score.value must be of type Score not{}'.format(type(value)))
        self._score = value


class Timewise(XMLScoreTimewise):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._measures = [].copy()
        self._score = None

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

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, Score):
            raise TypeError('score.value must be of type Score not{}'.format(type(value)))
        self._score = value
