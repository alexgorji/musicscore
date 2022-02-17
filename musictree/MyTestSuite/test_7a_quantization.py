from pathlib import Path

from musicxml.xmlelement.xmlelement import XMLAccent

from musictree.chord import Chord
from musictree.part import Part
from musictree.quarterduration import QuarterDuration
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestHelloWorldQuantization(IdTestCase):
    def test_export_hello_world_quantization(self):
        """
        Tester creates a timewise score
        """
        s = Score()
        """
        He adds a list of complicated quarter_durations
        """
        p = s.add_child(Part('p1'))
        import random
        random.seed(11)
        quarter_durations = []
        while sum(quarter_durations) < 40:
            quarter_durations.append(QuarterDuration(random.random() + random.randint(0, 3)))
        quarter_durations.append(44 - sum(quarter_durations))
        """
        He sets the possible subdivisions for all beats with quarter_duration and omits quintuplets and septuplets:
        """
        s.set_possible_subdivisions([2, 3, 4, 6, 8])
        """
        He adds chords with quarter_durations and writes each quarter_duration as lyrics
        """
        for qd in quarter_durations:
            ch = Chord(midis=71, quarter_duration=qd)
            ch.add_lyric(round(float(ch.quarter_duration), 2))
            p.add_chord(ch)
        """
        He calls quantize method to start quantization
        """
        p.quantize()
        p.split_not_writable_chords()
        s.update()
        """
        ... and exports the xm
        """
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)
