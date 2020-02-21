import os
from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.midi import G, C
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treeclef import ALL_CLEFS, SUPER_HIGH_TREBLE_CLEF, SUPER_LOW_BASS_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat()
        for clef in ALL_CLEFS:
            if clef not in [SUPER_HIGH_TREBLE_CLEF, SUPER_LOW_BASS_CLEF]:
                for midi in clef.optimal_range:
                    if not midi:
                        if clef.optimal_range.index(midi) == 0:
                            midi = G(0)
                        else:
                            midi = C(8)
                    sf.add_chord(TreeChord(quarter_duration=2, midis=[midi]))
                sf.chords[-2].add_clef(clef)
        xml = path + '_test_1.xml'
        sf.to_stream_voice().add_to_score(self.score)
        self.score.finish()
        self.score.to_partwise()
        self.score.write(xml)
