from musicscore.dtd.dtd import Choice, Element
from musicscore.musicxml.attributes.enclosure import Enclosure
from musicscore.musicxml.attributes.optional_unique_id import OptionalUniqueId
from musicscore.musicxml.attributes.placement import Placement
from musicscore.musicxml.attributes.printstyle import PrintStyleAlign
from musicscore.musicxml.attributes.textdecoration import TextDecoration
from musicscore.musicxml.types.complextypes.complextype import ComplexType, Empty
from musicscore.musicxml.types.complextypes.othertext import ComplexTypeOtherText


class P(Empty):
    _TAG = 'p'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PP(Empty):
    _TAG = 'pp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PPP(Empty):
    _TAG = 'ppp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PPPP(Empty):
    _TAG = 'pppp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PPPPP(Empty):
    _TAG = 'ppppp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PPPPPP(Empty):
    _TAG = 'pppppp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class F(Empty):
    _TAG = 'f'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FF(Empty):
    _TAG = 'ff'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FFF(Empty):
    _TAG = 'fff'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FFFF(Empty):
    _TAG = 'ffff'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FFFFF(Empty):
    _TAG = 'fffff'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FFFFFF(Empty):
    _TAG = 'ffffff'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MP(Empty):
    _TAG = 'mp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MF(Empty):
    _TAG = 'mf'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SF(Empty):
    _TAG = 'sf'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SFP(Empty):
    _TAG = 'sfp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SFPP(Empty):
    _TAG = 'sfpp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FP(Empty):
    _TAG = 'fp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class RF(Empty):
    _TAG = 'rf'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class RFZ(Empty):
    _TAG = 'rfz'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SFZ(Empty):
    _TAG = 'sfz'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SFFZ(Empty):
    _TAG = 'sffz'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class FZ(Empty):
    _TAG = 'fz'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class N(Empty):
    _TAG = 'n'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class PF(Empty):
    _TAG = 'pf'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class SFZP(Empty):
    _TAG = 'sfzp'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class OtherDynamics(ComplexTypeOtherText):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='other_dynamics', *args, **kwargs)


class ComplexTypeDynamics(ComplexType, PrintStyleAlign, Placement, TextDecoration, Enclosure, OptionalUniqueId):
    """
    Dynamics can be associated either with a note or a general musical direction. To avoid inconsistencies between and
    amongst the letter abbreviations for dynamics (what is sf vs. sfz, standing alone or with a trailing dynamic that
    is not always piano), we use the actual letters as the names of these dynamic elements. The other-dynamics element
    allows other dynamic marks that are not covered here, but many of those should perhaps be included in a more general
    musical direction element. Dynamics elements may also be combined to create marks not covered by a single element,
    such as sfmp.

    These letter dynamic symbols are separated from crescendo, decrescendo, and wedge indications. Dynamic
    representation is inconsistent in scores. Many things are assumed by the composer and left out, such as returns to
    original dynamics. Systematic representations are quite complex: for example, Humdrum has at least 3 representation
    formats related to dynamics. The MusicXML format captures what is in the score, but does not try to be optimal for
    analysis or synthesis of dynamics.
    """

    _DTD = Choice(
        Element(P),
        Element(PP),
        Element(PPP),
        Element(PPPP),
        Element(PPPPP),
        Element(PPPPPP),
        Element(F),
        Element(FF),
        Element(FFF),
        Element(FFFF),
        Element(FFFFF),
        Element(FFFFFF),
        Element(MP),
        Element(MF),
        Element(SF),
        Element(SFP),
        Element(SFPP),
        Element(FP),
        Element(RF),
        Element(RFZ),
        Element(SFZ),
        Element(SFFZ),
        Element(FZ),
        Element(N),
        Element(PF),
        Element(SFZP),
        Element(OtherDynamics),
        min_occurrence=0,
        max_occurrence=None
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
        self.placement = 'below'


class Dynamics(ComplexTypeDynamics):
    _TAG = 'dynamics'
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)