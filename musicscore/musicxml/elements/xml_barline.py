from musicscore.musicxml.attributes.barline import BarlineAttributes


class XMLBarline(BarlineAttributes):
    """If a barline is other than a normal single barline, it should be represented by a barline type that describes it.
    This includes information about repeats and multiple endings, as well as line style. Barline data is on the same
    level as the other musical data in a score - a child of a measure in a partwise score, or a part in a timewise
    score. This allows for barlines within measures, as in dotted barlines that subdivide measures in complex meters. The two
    fermata elements allow for fermatas on both sides of the barline (the lower one inverted). If no location is
    specified, the right barline is the default.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(tag='barline', *args, **kwargs)

