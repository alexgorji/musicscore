from unittest import TestCase

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
import os

from musicscore.musicxml.elements.note import Notations
from musicscore.musicxml.types.complextypes.harmonic import Artificial, BasePitch, TouchingPitch
from musicscore.musicxml.types.complextypes.notations import Technical
from musicscore.musicxml.types.complextypes.technical import Harmonic

path = str(os.path.abspath(__file__).split('.')[0])


class Test(TestCase):
    def setUp(self) -> None:
        self.score = TreeScoreTimewise()

    def test_1(self):
        sf = SimpleFormat(quarter_durations=[4], midis=[(60, 65)])
        chord = sf.chords[0]
        notations = chord.add_child(Notations())
        technical = notations.add_child(Technical())
        harmonic = technical.add_child(Harmonic())
        harmonic.add_child(Artificial())
        harmonic.add_child(TouchingPitch())

        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_1.xml'
        # self.score.write(xml_path)

    def test_2(self):
        sf = SimpleFormat(quarter_durations=[1.5, 2, 3, 2.33, 3.66], midis=5 * [60])
        for chord in sf.chords:
            chord.add_harmonic(5)
        sf.to_stream_voice().add_to_score(self.score)

        xml_path = path + '_test_2.xml'
        self.score.write(xml_path)
