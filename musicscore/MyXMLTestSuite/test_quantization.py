import random
from pathlib import Path

from musicscore import Score, QuarterDuration, SimpleFormat, Part
from musicscore.tests.test_metronome import TestCase


class TestQuantization(TestCase):
    def test_complex_quantization(self):
        s = Score()
        random.seed(11)
        quarter_durations = []
        while sum(quarter_durations) < 40:
            quarter_durations.append(QuarterDuration(random.random() + random.randint(0, 3)))
        quarter_durations.append(QuarterDuration(44 - sum(quarter_durations)))

        p = s.add_child(Part('p1'))
        chords = SimpleFormat(quarter_durations=quarter_durations).chords
        [ch.add_lyric(round(float(ch.quarter_duration), 2)) for ch in chords]
        [ch.add_words(str(i+1)) for i, ch in enumerate(chords)]
        [p.add_chord(ch) for ch in chords]
        p.get_quantized = True

        p = s.add_child(Part('p2'))
        p.set_possible_subdivisions([8, 4, 2, 3])
        chords = SimpleFormat(quarter_durations=quarter_durations).chords
        [ch.add_words(str(i + 1)) for i, ch in enumerate(chords)]
        [p.add_chord(ch) for ch in chords]
        p.get_quantized = True

        p = s.add_child(Part('p3'))
        p.set_possible_subdivisions([4, 2])
        chords = SimpleFormat(quarter_durations=quarter_durations).chords
        [ch.add_words(str(i + 1)) for i, ch in enumerate(chords)]
        [p.add_chord(ch) for ch in chords]
        p.get_quantized = True

        p = s.add_child(Part('p4'))
        p.set_possible_subdivisions([2])
        chords = SimpleFormat(quarter_durations=quarter_durations).chords
        [ch.add_words(str(i + 1)) for i, ch in enumerate(chords)]
        [p.add_chord(ch) for ch in chords]
        p.get_quantized = True

        p = s.add_child(Part('p5'))
        p.set_possible_subdivisions([1])
        chords = SimpleFormat(quarter_durations=quarter_durations).chords
        [ch.add_words(str(i + 1)) for i, ch in enumerate(chords)]
        [p.add_chord(ch) for ch in chords]
        p.get_quantized = True

        path = Path(__file__).with_suffix('.xml')
        s.export_xml(path=path)
