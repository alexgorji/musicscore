import uuid
from pathlib import Path

from musicscore import QuarterDurationIsNotWritable, Part, QuarterDuration, Chord, Score
from musicscore.exceptions import ChordTestError
from musicscore.tests.util import IdTestCase, create_test_xml_paths
from musicscore.tests.util_subdivisions import generate_subdivsion_test_patterns

path = Path(__file__)


class TestWritingSubdivisions(IdTestCase):

    def test_generate_patterns_1(self):
        expected = [
            (1, 4),
            (2, 3),
            (3, 2),
            (4, 1),
            (1, 1, 3),
            (1, 2, 2),
            (1, 3, 1),
            (2, 1, 2),
            (2, 2, 1),
            (3, 1, 1)
        ]
        assert list(generate_subdivsion_test_patterns(5)) == expected

    def test_generate_patterns_2(self):
        expected = [
            (1, 5),
            (2, 4),
            (3, 3),
            (4, 2),
            (5, 1),
            (1, 1, 4),
            (1, 2, 3),
            (1, 3, 2),
            (1, 4, 1),
            (2, 1, 3),
            (2, 2, 2),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1),
            (4, 1, 1)
        ]
        assert list(generate_subdivsion_test_patterns(6, remove_larger_subdivision=False)) == expected
        expected = [
            (1, 5),
            (5, 1),
            (1, 1, 4),
            (1, 2, 3),
            (1, 3, 2),
            (1, 4, 1),
            (2, 1, 3),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1),
            (4, 1, 1)
        ]
        assert list(generate_subdivsion_test_patterns(6, True)) == expected

    def write_and_test_subdivision(self, subdivision):
        for pattern in generate_subdivsion_test_patterns(subdivision, remove_larger_subdivision=True):
            p = Part(f'p{uuid.uuid4()}')
            p.add_measure([1, 4])
            qds = [QuarterDuration(x, subdivision) for x in pattern]
            [p.add_chord(Chord(71, qd)) for qd in qds]
            measure = p.get_children()[-1]
            try:
                measure.finalize()
                for ch in measure.get_chords():
                    try:
                        ch.check_printed_duration()
                        ch.check_number_of_beams()
                    except ChordTestError as err:
                        print(qds)
                        print([ch.quarter_duration for ch in measure.get_chords()])
                        print(err)

            except QuarterDurationIsNotWritable as err:
                print(qds)
                print(err)

    def test_write_quarter_upto_7(self):
        for subdivision in range(3, 8):
            self.write_and_test_subdivision(subdivision)

    def test_write_quarter_32nd(self):
        self.write_and_test_subdivision(8)

    def test_write_quarter_9(self):
        self.write_and_test_subdivision(9)

    def test_write_quarter_10(self):
        self.write_and_test_subdivision(10)

    def test_write_quarter_11(self):
        self.write_and_test_subdivision(11)

    def test_write_quarter_12(self):
        self.write_and_test_subdivision(12)

    def test_write_quarter_13(self):
        self.write_and_test_subdivision(13)

    def test_write_quarter_14(self):
        self.write_and_test_subdivision(14)

    def test_write_quarter_15(self):
        self.write_and_test_subdivision(15)

    def test_write_quarter_16(self):
        self.write_and_test_subdivision(16)

    def test_write_quarter_32(self):
        self.write_and_test_subdivision(32)


class TestWriteScoreWithSubdivisions(IdTestCase):
    def write_subdivision_to_file(self, subdivision):
        score = Score()
        p = score.add_part('p1')
        p.add_measure([1, 4])
        for pattern in generate_subdivsion_test_patterns(subdivision, remove_larger_subdivision=True):
            chords = [Chord(60, qd) for qd in [QuarterDuration(x, subdivision) for x in pattern]]
            [ch.add_lyric(x) for ch, x in zip(chords, pattern)]
            [p.add_chord(ch) for ch in chords]
        xml_path = create_test_xml_paths(path, f'{subdivision}')[0]
        score.export_xml(xml_path)

    def test_write_quarter_32nd(self):
        self.write_subdivision_to_file(8)

    def test_write_quarter_9(self):
        self.write_subdivision_to_file(9)

    def test_write_quarter_10(self):
        self.write_subdivision_to_file(10)

    def test_write_quarter_11(self):
        self.write_subdivision_to_file(11)

    def test_write_quarter_12(self):
        self.write_subdivision_to_file(12)

    def test_write_quarter_13(self):
        self.write_subdivision_to_file(13)

    def test_write_quarter_14(self):
        self.write_subdivision_to_file(14)

    def test_write_quarter_15(self):
        self.write_subdivision_to_file(15)

    def test_write_quarter_16(self):
        self.write_subdivision_to_file(16)

    def test_write_quarter_32(self):
        self.write_subdivision_to_file(32)
