from pathlib import Path
from unittest import TestCase

from musictree.accidental import Accidental
from musictree.chord import Chord
from musictree.measure import generate_measures
from musictree.midi import Midi
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase
from musictree.time import Time


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
