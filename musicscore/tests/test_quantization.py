from fractions import Fraction
from pathlib import Path
import random
from unittest import TestCase

from musicscore.beat import Beat
from musicscore.chord import Chord
from musicscore.part import Part
from musicscore.quarterduration import QuarterDuration
from musicscore.score import Score
from musicscore.staff import Staff
from musicscore.tests.util import XMLTestCase
from musicscore.util import lcm
from musicscore.voice import Voice


class TestQuantization(TestCase):
    def test_init_with_get_quantized_argument(self):
        b = Beat(get_quantized=True)
        self.assertTrue(b.get_quantized)
        v = Voice(get_quantized=True)
        self.assertTrue(v.get_quantized)
        s = Staff(get_quantized=True)
        self.assertTrue(s.get_quantized)
        p = Part(id="P1", get_quantized=True)
        self.assertTrue(p.get_quantized)
        sc = Score(get_quantized=True)
        self.assertTrue(sc.get_quantized)

    def test_get_and_set_possible_subdivisions(self):
        s = Score()
        p = s.add_child(Part("p1"))
        m = p.add_measure()
        s = m.get_children()[0]
        v = s.get_children()[0]
        beats = v.get_children()
        for beat in beats:
            assert beat.get_possible_subdivisions() == [2, 3, 4, 5, 6, 7, 8]
        beats[0].quarter_duration = 1 / 2
        assert beats[0].get_possible_subdivisions() == [2, 3, 4, 5]
        beats[0].quarter_duration = 1 / 4
        assert beats[0].get_possible_subdivisions() == [2, 3]
        beats[0].quarter_duration = 1 / 8
        assert beats[0].get_possible_subdivisions() is None
        v.set_possible_subdivisions([2, 3, 4, 6], beat_quarter_duration=1)
        beats[1].set_possible_subdivisions([2, 4])
        assert beats[0].get_possible_subdivisions() is None
        assert beats[1].get_possible_subdivisions() == [2, 4]
        for beat in beats[2:]:
            assert beat.get_possible_subdivisions() == [2, 3, 4, 6]

        with self.assertRaises(ValueError):
            beats[1].set_possible_subdivisions([2, 4], beat_quarter_duration=0.5)

    def test_quantize_attribute(self):
        s = Score()
        p = s.add_child(Part("p1"))
        m = p.add_measure()

        st = m.get_children()[0]

        v = st.get_children()[0]
        beats = v.get_children()

        assert s.get_quantized is False
        assert p.get_quantized is False
        assert m.get_quantized is False
        assert st.get_quantized is False
        assert v.get_quantized is False
        for b in beats:
            assert b.get_quantized is False

        s.get_quantized = True
        assert p.get_quantized is True
        assert m.get_quantized is True
        assert st.get_quantized is True
        assert v.get_quantized is True
        for b in beats:
            assert b.get_quantized is True

        st.get_quantized = False
        assert s.get_quantized is True
        assert p.get_quantized is True
        assert m.get_quantized is True
        assert st.get_quantized is False
        assert v.get_quantized is False
        for b in beats:
            assert b.get_quantized is False

        p.get_quantized = False
        m.get_quantized = True
        st.get_quantized = False
        v.get_quantized = True
        beats[0].get_quantized = False
        beats[1].get_quantized = True
        beats[2].get_quantized = False
        beats[3].get_quantized = True

        assert s.get_quantized is True
        assert p.get_quantized is False
        assert m.get_quantized is True
        assert st.get_quantized is False
        assert v.get_quantized is True

    def test_simple_quantization(self):
        s = Score()
        p = s.add_child(Part("p1"))
        p.add_measure()
        p.add_chord(Chord(60, 0.2))
        p.add_chord(Chord(60, 3.8))
        assert [ch.quarter_duration for ch in p.get_chords()] == [0.2, 0.8, 3]
        b = p.get_measure(1).get_staff(1).get_voice(1).get_beat(1)
        b.set_possible_subdivisions(subdivisions=[2, 3, 4])
        b.quantize_quarter_durations()
        assert [
            ch.quarter_duration
            for ch in p.get_measure(1).get_staff(1).get_voice(1).get_chords()
        ] == [0.25, 0.75, 3]
        assert [
            ch.offset for ch in p.get_measure(1).get_staff(1).get_voice(1).get_chords()
        ] == [0, 0.25, 0]

    def test_complex_quantization(self):
        s = Score()
        s.set_possible_subdivisions([2, 3, 4, 6, 8])
        p = s.add_child(Part("p1"))
        random.seed(11)
        quarter_durations = []
        while sum(quarter_durations) < 40:
            quarter_durations.append(
                QuarterDuration(random.random() + random.randint(0, 3))
            )
        quarter_durations.append(44 - sum(quarter_durations))

        for qd in quarter_durations:
            p.add_chord(Chord(midis=60, quarter_duration=qd))
        for beat in [
            b
            for m in p.get_children()
            for st in m.get_children()
            for v in st.get_children()
            for b in v.get_children()
        ]:
            beat.quantize_quarter_durations()
        # p.get_quantized = True
        for measure in p.get_children():
            v = measure.get_staff(1).get_voice(1)
            for b in v.get_children():
                qds = [ch.quarter_duration for ch in b.get_children()]
                div = lcm([qd.denominator for qd in qds])
                if div != 1:
                    assert div in [2, 3, 4, 6, 8]

    def test_add_short_chord(self):
        s = Score()
        p = s.add_part("part-1")
        p.add_chord(Chord(60, 9 / 20))
        p.get_quantized = True
        p.finalize()
        self.assertEqual(
            [chord.quarter_duration for chord in p.get_chords()], [3 / 7, 4 / 7, 3 / 1]
        )

    def test_part_quantization(self):
        s = Score()
        s.set_possible_subdivisions([2, 3, 4, 6, 8])
        p = s.add_child(Part("p1"))
        for qd in [2, 2 / 7, 1, 5 / 7]:
            p.add_chord(Chord(60, qd))
        p.get_quantized = True
        p.finalize()
        assert [ch.quarter_duration for ch in p.get_chords()] == [
            2,
            1 / 4,
            3 / 4,
            1 / 4,
            3 / 4,
        ]
        assert p.get_measure(1).get_divisions() == 4
        assert [ch.notes[0].xml_duration.value_ for ch in p.get_chords()] == [
            8,
            1,
            3,
            1,
            3,
        ]


path = Path(__file__)


class TestQuantizationWithAfterGraceNotes(XMLTestCase):
    def test_quantization_with_grace_notes(self):
        s = Score()
        s.get_quantized = True
        p = s.add_child(Part("p1"))
        p.set_possible_subdivisions([2, 3, 4])
        p.add_measure(time=(1, 4))
        for qd in [0, 0, 1 / 2, 0, 0, 1 / 2 - 1 / 8, 1 / 16, 1 / 16]:
            p.add_chord(Chord(60, qd))
        b = p.get_beat(1, 1, 1, 1)
        b.quantize_quarter_durations()
        self.assertEqual(
            [ch.quarter_duration for ch in b.get_chords()],
            [0, 0, 1 / 2, 0, 0, 1 / 2, 0, 0],
        )
        s.finalize()
        with self.file_path(path, "with_grace_notes") as xml_path:
            s.export_xml(xml_path)

    def test_quantization_with_grace_notes_complex(self):
        s = Score()
        s.get_quantized = True
        p = s.add_child(Part("p1"))
        durations = [
            Fraction(128, 675),
            Fraction(64, 135),
            Fraction(64, 675),
            Fraction(64, 225),
            Fraction(256, 675),
            Fraction(256, 675),
            Fraction(1024, 3375),
            Fraction(512, 3375),
            Fraction(256, 3375),
            Fraction(256, 1125),
            Fraction(128, 3375),
            Fraction(256, 3375),
            Fraction(128, 1125),
            Fraction(512, 3375),
            Fraction(128, 675),
            Fraction(256, 3375),
            Fraction(64, 1125),
            Fraction(64, 675),
            Fraction(128, 3375),
            Fraction(64, 3375),
            Fraction(64, 375),
            Fraction(64, 1125),
            Fraction(256, 1125),
            Fraction(64, 225),
            Fraction(128, 1125),
            Fraction(16, 375),
        ]
        for qd in durations:
            p.add_chord(Chord(60, qd))
        # s.finalize()
        with self.file_path(path, "with_grace_notes_complex") as xml_path:
            s.export_xml(xml_path)
