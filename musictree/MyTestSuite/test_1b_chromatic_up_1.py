from pathlib import Path
from unittest import TestCase

from musictree.accidental import Accidental
from musictree.chord import Chord
from musictree.measure import generate_measures
from musictree.midi import Midi
from musictree.part import Part
from musictree.score import Score
from musictree.time import Time


class TestHelloWorld(TestCase):
    def test_chromatic_up_quarter_grid(self):
        """
        Scale chromatically up with different quarter_durations and time signatures
        """
        s = Score()
        p = s.add_child(Part('p1'))
        quarter_durations = list(range(10, 0, -1))
        """
        Adding measures
        """
        measures = generate_measures(times=[Time(qd, 4) for qd in quarter_durations])
        for m in measures:
            p.add_child(m)
        """
        Adding chords
        """
        min_midi = 60
        for m, qd in zip(measures, quarter_durations):
            m.add_chord(Chord(quarter_duration=qd, midis=Midi(min_midi + 10 - qd, accidental=Accidental(mode='sharp'))))
        """
        Exporting
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
        # assert diff_xml(xml_path) == []
