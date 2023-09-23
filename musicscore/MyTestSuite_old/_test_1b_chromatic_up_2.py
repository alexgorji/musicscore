from pathlib import Path
from unittest import TestCase

from musicscore.accidental import Accidental
from musicscore.chord import Chord
from musicscore.measure import generate_measures
from musicscore.midi import Midi
from musicscore.part import Part
from musicscore.score import Score
from musicscore.tests.util import IdTestCase
from musicscore.time import Time


class TestHelloWorld(IdTestCase):
    def test_chromatic_up_quarter_grid(self):
        """
        Scale chromatically up with different quarter_durations and time signatures (reversed order)
        """
        s = Score()
        p = s.add_child(Part('p1'))
        quarter_durations = list(range(10, 0, -1))
        """
        Adding measures
        """
        for qd in reversed(quarter_durations):
            p.add_measure(time=Time(qd, 4))
        """
        Adding chords
        """
        min_midi = 60
        for qd in quarter_durations:
            p.add_chord(Chord(quarter_duration=qd, midis=Midi(min_midi + 10 - qd, accidental=Accidental(mode='sharp'))))

        """
        Exporting
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
        # assert diff_xml(xml_path) == []
