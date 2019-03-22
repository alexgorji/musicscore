from musicscore.dtd.dtd import Sequence, Element
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.partlist import ComplexTypePartList
from musicscore.musicxml.types.complextypes.scorepart import Identification


class Work(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='work', *args, **kwargs)
        raise NotImplementedError('Work')


class MovementNumber(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='movement-number', *args, **kwargs)
        raise NotImplementedError('MovementNumber')


class MovementTitle(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='movement-title', *args, **kwargs)
        raise NotImplementedError('MovementTitle')


class Defaults(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='defaults', *args, **kwargs)
        raise NotImplementedError('Defaults')


class Credit(XMLElement):
    def __init__(self, *args, **kwargs):
        super().__init__(tag='credit', *args, **kwargs)
        raise NotImplementedError('Credit')


class PartList(ComplexTypePartList):

    def __init__(self, *args, **kwargs):
        super().__init__(tag='part-list', *args, **kwargs)


"""
The score-header group contains basic score metadata about the work and movement, score-wide defaults for layout and 
fonts, credits that appear on the first or following pages, and the part list.
"""
ScoreHeader = Sequence(
    Element(Work, min_occurrence=0),
    Element(MovementNumber, min_occurrence=0),
    Element(MovementTitle, min_occurrence=0),
    Element(Identification, min_occurrence=0),
    Element(Defaults, min_occurrence=0),
    Element(Credit, min_occurrence=0, max_occurrence=None),
    Element(PartList)
)
