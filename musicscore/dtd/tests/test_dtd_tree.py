from unittest import TestCase
from musicscore.dtd.dtd import Sequence, Choice, Element, Group
from musicscore.dtd.note import Grace, FullNote, Cue, Duration, Instrument, EditorialVoice, Type, Dot, Accidental, \
    TimeModification, Stem, Notehead, NotheadText, Staff, Beam, Notations, Play, Lyric, Tie

import copy


class TestDTDTree(TestCase):
    def setUp(self):
        self.dtd = (
            Sequence(
                Choice(
                    Sequence(
                        Element(Grace),
                        Choice(
                            Sequence(
                                Group(FullNote)
                            ),
                            Sequence(
                                Group(FullNote),
                                Element(Tie, 0, 2)
                            ),
                            Sequence(
                                Element(Cue),
                                Group(FullNote)
                            )
                        )
                    ),
                    Sequence(
                        Element(Cue),
                        Group(FullNote),
                        Group(Duration)
                    ),
                    Sequence(
                        Group(FullNote),
                        Group(Duration),
                        Element(Tie, 0, 2)
                    )
                ),
                Element(Instrument, 0),
                Group(EditorialVoice),
                Element(Type, 0),
                Element(Dot, 0, None),
                Element(Accidental, 0),
                Element(TimeModification, 0, None),
                Element(Stem, 0),
                Element(Notehead, 0),
                Element(NotheadText, 0),
                Group(Staff, 0),
                Element(Beam, 0, 8),
                Element(Notations, 0, None),
                Element(Lyric, 0, None),
                Element(Play, 0)
            )
        )

    def test_dtd_leaves(self):
        leaves = self.dtd.get_leaves(key=lambda child: (type(child).__name__, child._type.__name__))
        # print(leaves)

    def test_expand(self):
        sequence_1 = Sequence(Element(Beam), Element(Play), Element(Notehead))
        sequence_2 = Sequence(Element(Stem), Element(Lyric))
        choice = Choice(sequence_1, sequence_2)

        all_nodes = self.dtd.dump()
        # all_nodes.reverse()

        output = [self.dtd.clone()]

        for node in all_nodes:
            if isinstance(node, Choice):
                for i in range(len(node.get_children()) - 1):
                    output.append(self.dtd.clone())

        for clone in output:
            for node in clone.traverse():
                pass
        print(len(output))

        # for el in choice.get_layer(2):
        #     print(el.id)
        # for el in choice.traverse():
        #     print(el.id)
        # print(sequence_1.expand())

        # print(choice.expand())

        # choice = Choice(Element(Beam), Element(Play))
        # dtd = Sequence(Element(Stem), choice, Element(Notehead))
        # print(choice.expand())
        # print(dtd.expand())
