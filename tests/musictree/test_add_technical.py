from unittest import TestCase
import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
from musicscore.musicxml.types.complextypes.hole import HoleClosed
from musicscore.musicxml.types.complextypes.technical import Hole, UpBow

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        xml_path = path + '_test_1.xml'
        durations = [2, 1, 0.5, 0.25, 0.25, 4, 2, 3]
        sf = SimpleFormat(quarter_durations=durations)
        for chord in sf.chords:
            technical = UpBow()
            chord.add_technical_object(technical)

        sf.to_stream_voice().add_to_score(self.score)
        self.score.write(xml_path)
        # TestScore().assert_template(xml_path)

    # def test_2(self):
    #     xml_path = path + '_test_2.xml'
    #     articulations = ['accent', 'strong-accent', 'staccato', 'tenuto', 'detached-lagato', 'staccatissimo',
    #                      'spiccato', 'scoop', 'plop', 'doit', 'falloff', 'breath-mark', 'caesura', 'stress', 'unstress']
    #     durations = len(articulations) * [1.25]
    #     sf = SimpleFormat(durations=durations)
    #     for index, chord in enumerate(sf.chords):
    #         chord.add_articulation(articulations[index])
    #
    #     sf.to_stream_voice().add_to_score(self.score)
    #     self.score.write(xml_path)
    #     TestScore().assert_template(xml_path)
