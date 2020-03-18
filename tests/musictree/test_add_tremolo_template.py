from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat, TreeChord
from musicscore.musictree.treechordflags1 import FingerTremoloFlag1, PercussionFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.note import TimeModification, Stem
from musicscore.musicxml.types.complextypes.timemodification import ActualNotes, NormalNotes

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + "_test_1.xml"
        sf = SimpleFormat(midis=[60, 63], quarter_durations=[0.5, 0.5, 3, 4, 4, 4])

        sf.chords[0].set_manual_type('quarter')
        sf.chords[1].set_manual_type('quarter')

        sf.chords[1].add_child(Stem('none'))
        sf.chords[0].quarter_duration *= 2
        # sf.chords[1].add_child(Stem('up'))

        # sf.chords[0].add_bracket(type='start', line_end='down', relative_x=0)
        # sf.chords[2].add_bracket(type='stop', line_end='none')

        sf.chords[0].add_words('\uE227', font_family='bravura', font_size=16, relative_x=30, relative_y=-50)

        tm = TimeModification()
        tm.add_child(ActualNotes(0))
        tm.add_child(NormalNotes(1))
        sf.chords[1].add_child(tm)

        sf.to_stream_voice().add_to_score(self.score)

        self.score.write(xml_path)

