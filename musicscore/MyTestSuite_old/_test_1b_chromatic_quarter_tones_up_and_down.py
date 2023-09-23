from pathlib import Path
from unittest import TestCase

from musicscore import SimpleFormat
from musicscore.accidental import Accidental
from musicscore.chord import Chord
from musicscore.measure import generate_measures
from musicscore.midi import Midi
from musicscore.part import Part
from musicscore.score import Score
from musicscore.time import Time


class TestHelloChromatics(TestCase):
    def test_chromatic_quarter_tone(self):
        """
        Up and down chromatic scales with quarter tones
        """
        s = Score()
        p = s.add_child(Part('p1'))
        """
        Using SimpleFormat:
        """
        midi_values = [val / 2 for val in range(120, 120 + 48 + 1)]
        midi_values = midi_values + list(reversed(midi_values[:-1]))
        print(midi_values)
        sf = SimpleFormat(midis=midi_values)
        for chord in sf.chords:
            p.add_chord(chord)
        xml_path = Path(__file__).with_suffix('.xml')
        s.export_xml(xml_path)

        # measures = generate_measures(times=[Time(qd, 4) for qd in quarter_durations])
        # for m in measures:
        #     p.add_child(m)
        # """
        # Adding chords
        # """
        # min_midi = 60
        # for m, qd in zip(measures, quarter_durations):
        #     m._add_chord(Chord(quarter_duration=qd, midis=Midi(min_midi + 10 - qd, accidental=Accidental(mode='sharp'))))
        # """
        # Exporting
        # """
        # xml_path = Path(__file__).with_suffix('.xml')
        # s.export_xml(xml_path)
