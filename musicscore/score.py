from musicscore.musicxml.elements.xml_partwise import XMLScorePartwise, XMLMeasurePartwise, XMLPartPartwise
from musicscore.musicxml.elements.xml_timewise import XMLScoreTimewise


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


class Partwise(object):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Timewise(object):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# class Score(XMLScorePartwise):
#     """"""

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._measures = []
#
#     @property
#     def measures(self):
#         return self._measures
#
#     @measures.setter
#     def measures(self, value):
#         if not isinstance(value, list):
#             raise TypeError('measures.value must be of type list not{}'.format(type(value)))
#         for element in value:
#             if not isinstance(element, Measure):
#                 raise TypeError('measures.value.element  must be of type Measure not{}'.format(type(element)))
#         self._measures = value
#
#
# class Part(XMLPartPartwise):
#     """"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#
# class Measure(XMLMeasurePartwise):
#     """"""
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
