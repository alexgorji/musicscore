from musicscore.dtd.dtd import Sequence, Element, GroupReference
from musicscore.musicxml.groups.layout import Layout
from musicscore.musicxml.types.complextypes.appearance import ComplexTypeAppearance
from musicscore.musicxml.types.complextypes.complextype import ComplexType, EmptyFont
from musicscore.musicxml.types.complextypes.lyricfont import ComplexTypeLyricFont
from musicscore.musicxml.types.complextypes.lyriclanguage import ComplexTypeLyricLanguage
from musicscore.musicxml.types.complextypes.scaling import ComplexTypeScaling


class Scaling(ComplexTypeScaling):
    _TAG = 'scaling'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class Appearance(ComplexTypeAppearance):
    """"""

    _TAG = 'appearance'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class MusicFont(EmptyFont):
    """"""

    _TAG = 'music-font'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class WordFont(EmptyFont):
    """"""

    _TAG = 'word-font'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class LyricFont(ComplexTypeLyricFont):
    """"""

    _TAG = 'lyric-font'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class LyricLanguage(ComplexTypeLyricLanguage):
    """"""

    _TAG = 'lyric-language'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypeDefaults(ComplexType):
    """
    The defaults type specifies score-wide defaults for scaling, layout, and appearance.
    """

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)

    _DTD = Sequence(
        Element(Scaling, min_occurrence=0),
        GroupReference(Layout),
        Element(Appearance, 0),
        Element(MusicFont, 0),
        Element(WordFont, 0),
        Element(LyricFont, 0, None),
        Element(LyricLanguage, 0, None)
    )
