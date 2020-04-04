from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import BASS_CLEF, TREBLE_CLEF, ALTO_CLEF, TENOR_CLEF, PERCUSSION_CLEF, \
    HIGH_TREBLE_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from tests.score_templates.xml_test_score import TestScore

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
        sf.chords[0].add_clef(BASS_CLEF)
        sf.chords[1].add_clef(TREBLE_CLEF)
        sf.chords[2].add_clef(PERCUSSION_CLEF)
        sf.chords[3].add_clef(ALTO_CLEF)
        sf.chords[4].add_clef(TENOR_CLEF)
        sf.chords[6].add_clef(TENOR_CLEF)
        sf.chords[7].add_clef(HIGH_TREBLE_CLEF)

        v = sf.to_stream_voice(1)
        v.add_to_score(self.score)

        result_path = path + '_test_1'
        self.score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
