from musicscore.dtd.dtd import Sequence, GroupReference, Choice, Element
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.printobject import PrintObject
from musicscore.musicxml.groups.common import Editorial
from musicscore.musicxml.elements.xml_element import XMLElement
from musicscore.musicxml.types.complextypes.arpeggiate import ComplexTypeArpeggiate
from musicscore.musicxml.types.complextypes.articulations import ComplexTypeArticulations
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.dynamics import Dynamics
from musicscore.musicxml.types.complextypes.fermata import ComplexTypeFermata
from musicscore.musicxml.types.complextypes.ornaments import ComplexTypeOrnaments
from musicscore.musicxml.types.complextypes.slide import ComplexTypeSlide
from musicscore.musicxml.types.complextypes.slur import ComplexTypeSlur
from musicscore.musicxml.types.complextypes.technical import ComplexTypeTechnical
from musicscore.musicxml.types.complextypes.tied import ComplexTypeTied
from musicscore.musicxml.types.complextypes.tuplet import ComplexTypeTuplet


class Tied(ComplexTypeTied):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Slur(ComplexTypeSlur):
    _TAG = 'slur'

    def __init__(self, type, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Tuplet(ComplexTypeTuplet):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Glissando(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='glissando', value=value, *args, **kwargs)
        raise NotImplementedError()


class Slide(ComplexTypeSlide):
    """"""
    _TAG = 'slide'

    def __init__(self, type, *args, **kwargs):
        super().__init__(tag=self._TAG, type=type, *args, **kwargs)


class Ornaments(ComplexTypeOrnaments):
    """"""
    _TAG = 'ornaments'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Technical(ComplexTypeTechnical):
    """"""

    _TAG = 'technical'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Articulations(ComplexTypeArticulations):
    """"""
    _TAG = 'articulations'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Fermata(ComplexTypeFermata):
    """"""
    _TAG = 'fermata'

    def __init__(self, value='normal', *args, **kwargs):
        super().__init__(tag=self._TAG, value=value, *args, **kwargs)


class Arpeggiate(ComplexTypeArpeggiate):
    """"""
    _TAG = 'arpeggiate'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class NonArpeggiate(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='non-arpeggiate', value=value, *args, **kwargs)
        raise NotImplementedError()


class AccidentalMark(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='accidental-mark', value=value, *args, **kwargs)
        raise NotImplementedError()


class OtherNotation(XMLElement):
    """"""

    def __init__(self, value, *args, **kwargs):
        super().__init__(tag='other-notation', value=value, *args, **kwargs)
        raise NotImplementedError()


class ComplexTypeNotations(ComplexType, PrintObject, OptionalUniqueId):
    """
    Notations refer to musical notations, not XML notations. Multiple notations are allowed in order to represent
    multiple editorial levels. The print-object attribute, added in Version 3.0, allows notations to represent details
    of performance technique, such as fingerings, without having them appear in the score.
    """
    _DTD = Sequence(
        GroupReference(Editorial),
        Choice(
            Element(Tied),
            Element(Slur),
            Element(Tuplet),
            Element(Glissando),
            Element(Slide),
            Element(Ornaments),
            Element(Technical),
            Element(Articulations),
            Element(Dynamics),
            Element(Fermata),
            Element(Arpeggiate),
            Element(NonArpeggiate),
            Element(AccidentalMark),
            Element(OtherNotation),
            min_occurrence=0,
            max_occurrence=None
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(tag='notations', *args, **kwargs)
