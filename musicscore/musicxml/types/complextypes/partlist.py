from musicscore.dtd.dtd import Sequence, Element, Choice
from musicscore.musicxml.types.complextypes.complextype import ComplexType
from musicscore.musicxml.types.complextypes.partgroup import ComplexTypePartGroup
from musicscore.musicxml.types.complextypes.scorepart import ComplexTypeScorePart


class ScorePart(ComplexTypeScorePart):
    """
    The score-part element is defined within a group due to its multiple uses within the part-list element.
    Each MusicXML part corresponds to a track in a Standard MIDI Format 1 file. The score-instrument elements are used
    when there are multiple instruments per track. The midi-device element is used to make a MIDI device or port
    assignment for the given track. Initial midi-instrument assignments may be made here as well.
    """
    _TAG = 'score-part'

    def __init__(self, id, *args, **kwargs):
        super().__init__(tag=self._TAG, id=id, *args, **kwargs)


class PartGroup(ComplexTypePartGroup):
    _TAG = 'part-group'

    def __init__(self, *args, **kwargs):
        super().__init__(tag=self._TAG, *args, **kwargs)


class ComplexTypePartList(ComplexType):
    """
    The part-list identifies the different musical parts in this movement. Each part has an ID that is used later within
    the musical data. Since parts may be encoded separately and combined later, identification elements are present at
    both the score and score-part levels. There must be at least one score-part, combined as desired with part-group
    elements that indicate braces and brackets. Parts are ordered from top to bottom in a score based on the order in
    which they appear in the part-list.
    """
    # _DTD = Sequence(
    #     Element(PartGroup, min_occurrence=0, max_occurrence=None),
    #     Element(ScorePart),
    #     Choice(
    #         Element(PartGroup),
    #         Element(ScorePart),
    #         min_occurrence=0, max_occurrence=None
    #     )
    # )
    _DTD = Sequence(
        Choice(Element(PartGroup, min_occurrence=0, max_occurrence=None),
               Element(ScorePart)
               ),
        Choice(
            Element(PartGroup),
            Element(ScorePart),
            min_occurrence=0, max_occurrence=None
        )
    )

    def __init__(self, tag, *args, **kwargs):
        super().__init__(tag=tag, *args, **kwargs)
