from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechordflags1 import PercussionFlag1, XFlag1
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.types.complextypes.articulations import Accent
from tests.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(quarter_durations=durations)
        for chord in sf.chords:
            articulation = Accent()
            chord.add_articulation_object(articulation)

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)

    def test_2(self):
        xml_path = path + '_test_2.xml'
        articulations = ['accent', 'strong-accent', 'staccato', 'tenuto', 'detached-legato', 'staccatissimo',
                         'spiccato', 'scoop', 'plop', 'doit', 'falloff', 'breath-mark', 'caesura', 'stress', 'unstress']
        durations = len(articulations) * [1.25]
        sf = SimpleFormat(quarter_durations=durations)
        for index, chord in enumerate(sf.chords):
            chord.add_articulation(articulations[index])

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        TestScore().assert_template(xml_path)
