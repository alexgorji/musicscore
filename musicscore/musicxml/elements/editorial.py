from musicscore.dtd.dtd import GroupReference, Sequence, Element
from musicscore.musicxml.types.complex_type import TypeLevel

Footnote = Sequence(

)


class Level(TypeLevel):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(tag='level', *args, **kwargs)


"""
The level element specifies editorial information for different MusicXML elements. It is defined within a group due to 
its multiple uses within the MusicXML schema.
"""
Level = Sequence(
    Element(Level)
)

"""
The editorial group specifies editorial information for a musical element.
"""
Editorial = Sequence(
    GroupReference(Footnote, min_occurrence=0),
    GroupReference(Level, min_occurrence=0)

)
