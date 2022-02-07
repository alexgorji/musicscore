from musictree.chord import Chord
from musictree.exceptions import IdHasAlreadyParentOfSameTypeError, IdWithSameValueExistsError
from musictree.measure import Measure
from musictree.part import Part, ScorePart, Id
from musictree.tests.util import IdTestCase


class TestId(IdTestCase):

    def test_id_refs(self):
        id1 = Id('p1')
        id2 = Id('p2')
        assert Id.__refs__ == [id1, id2]
        id3 = Id('p3')
        assert Id.__refs__ == [id1, id2, id3]
        id3.delete()
        assert Id.__refs__ == [id1, id2]
        Id('p3')

    def test_id_unique(self):
        Id('p1')
        id2 = Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p1')
        id3 = Id('p3')
        with self.assertRaises(IdWithSameValueExistsError):
            Id('p2')
        with self.assertRaises(IdWithSameValueExistsError):
            id3.value = 'p2'
        assert id3.value == 'p3'
        id2.delete()
        id3.value = 'p2'
        assert id3.value == 'p2'

    def test_id_parents(self):
        id_ = Id('p1')
        assert id_.get_parents() == []
        p = Part(id=id_)
        assert id_.get_parents() == [p, p.score_part]
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            Part(id=id_)
        with self.assertRaises(IdHasAlreadyParentOfSameTypeError):
            ScorePart(part=p)
        assert p.xml_object.id == p.score_part.xml_object.id == 'p1'
        id_.value = 'p2'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p2'
        p.id_ = 'p3'
        assert p.xml_object.id == p.score_part.xml_object.id == 'p3'


class TestPart(IdTestCase):
    def test_part_init(self):
        p = Part(id='p1')
        p.add_child(Measure(1))
        assert p.xml_object.id == 'p1'

    def test_part_name(self):
        p = Part(id='p1')
        assert p.name == 'p1'
        p = Part(id='p2', name='Part 1')
        assert p.name == 'Part 1'
        p.name = None
        assert p.name == 'p2'

    def test_part_and_score_part(self):
        p = Part(id='p1')
        assert isinstance(p.score_part, ScorePart)
        assert p.score_part.xml_object.id == p.xml_object.id

    def test_add_measure(self):
        p = Part('p1')
        m = p.add_measure()
        assert p.get_children()[-1] == m
        assert m.number == 1
        assert m.time.signatures == (4, 4)
        m = p.add_measure(time=(4, 3, 2, 1))
        assert p.get_children()[-1] == m
        assert m.number == 2
        assert m.time.signatures == (4, 3, 2, 1)
        m = p.add_measure()
        assert p.get_children()[-1] == m
        assert m.number == 3
        assert m.time.signatures == (4, 3, 2, 1)

    def test_part_add_measure_check_voice(self):
        """
        Test if Part.add_measure() adds a Measure with a Staff (value=None) and Voice (value=1)
        """
        p = Part('p1')
        m1 = p.add_measure()
        assert m1.get_staff(None) is not None
        assert m1.get_voice(staff=None, voice=1) is not None

    def test_part_set_current_measure(self):
        p = Part('p1')
        m1 = Measure(1)
        p.set_current_measure(1, 1, m1)
        assert p.get_current_measure(1, 1) == m1
        m2 = Measure(2)
        p.set_current_measure(1, 1, m2)
        assert p.get_current_measure(1, 1) == m2
        assert p.get_current_measure(1, 2) is None

        p = Part('p2')
        m1 = Measure(1)
        p.set_current_measure(None, 1, m1)
        assert p.get_current_measure(1, 1) == m1
        m2 = Measure(2)
        p.set_current_measure(1, 1, m2)
        assert p.get_current_measure(1, 1) == m2

    def test_part_get_current_measure_simple(self):
        p = Part('p1')
        m1 = p.add_measure()
        assert p.get_current_measure(staff=1, voice=1) == m1
        m2 = p.add_measure()
        m1.add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff=1, voice=1) == m1
        m1.add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff=1, voice=1) == m1
        assert m1.get_voice(staff=1, voice=1).is_filled
        m2.add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff=1, voice=1) == m2
        m3 = p.add_measure()
        m4 = p.add_measure()
        m4.add_chord(Chord(midis=60, quarter_duration=2))
        assert p.get_current_measure(staff=1, voice=1) == m4

    def test_part_get_current_measure_complex(self):
        p = Part('p1')
        assert p.get_current_measure(staff=None, voice=1) is None
        m1 = p.add_measure()
        m1.add_chord(Chord(midis=60, quarter_duration=4), staff=2, voice=2)
        assert p.get_current_measure(staff=1, voice=1) == m1
        assert p.get_current_measure(staff=1, voice=2) is None
        assert p.get_current_measure(staff=2, voice=1) == m1
        assert p.get_current_measure(staff=2, voice=1).get_voice(staff=2, voice=1).is_filled is False
        assert p.get_current_measure(staff=2, voice=2) == m1
        assert p.get_current_measure(staff=2, voice=2).get_voice(staff=2, voice=2).is_filled is True
        m1.add_voice(staff=1, voice=1)
        assert p.get_current_measure(staff=1, voice=1) == m1
        #
        m2 = p.add_measure()
        m2.add_chord(Chord(midis=60, quarter_duration=4), staff=2, voice=2)
        assert p.get_current_measure(staff=1, voice=1) == m1
        assert p.get_current_measure(staff=1, voice=2) is None
        assert p.get_current_measure(staff=2, voice=1) == m1
        assert p.get_current_measure(staff=2, voice=2) == m2

        m1 = Measure(1)
        m1.add_chord(Chord(midis=60, quarter_duration=1))
        p = Part('p2')
        p.add_child(m1)
        assert p.get_current_measure(staff=1, voice=1) == m1

    def test_part_add_chord_different_staves_and_voices(self):
        p = Part('p1')
        p.add_chord(Chord(60, 1))
        m = p.get_children()[0]
        assert m.get_voice(staff=1, voice=1) is not None
        p.add_chord(Chord(61, 2), staff=2, voice=4)
        for i in range(1, 5):
            assert m.get_voice(staff=2, voice=i) is not None
        p.add_chord(Chord(62, 3), staff=1, voice=1)
        assert [ch.quarter_duration for ch in m.get_voice(staff=1, voice=1).get_chords()] == [1, 3]
        assert [ch.midis[0].value for ch in m.get_voice(staff=1, voice=1).get_chords()] == [60, 62]
        assert [ch.quarter_duration for ch in m.get_voice(staff=2, voice=4).get_chords()] == [2]

    def test_part_add_chord_with_left_over(self):
        p = Part('p1')
        ch = Chord(60, 5)
        p.add_chord(ch)
        assert len(p.get_children()) == 2
        m1, m2 = p.get_children()
        assert p.get_current_measure(1, 1) == m2
        assert m1.get_voice(staff=1, voice=1).is_filled
        assert not m2.get_voice(staff=1, voice=1).is_filled

    def test_part_add_chord_to_full_measure(self):
        p = Part('p1')
        p.add_chord(Chord(60, 4))
        p.add_chord(Chord(60, 6))
        m1, m2, m3 = p.get_children()
        assert p.get_current_measure() == m3

    def test_part_add_chord_to_existing_measures(self):
        p = Part('p1')
        for _ in range(3):
            p.add_measure()
        m1, m2, m3 = p.get_children()
        assert p.get_current_measure() == m1
        p.add_chord(Chord(60, 5))
        assert p.get_current_measure() == m2


class TestScorePart(IdTestCase):

    def test_score_part_name(self):
        p = Part(id='p1')
        assert p.score_part.xml_part_name.value == p.name == 'p1'
        p.name = 'Part 1'
        assert p.score_part.xml_part_name.value == p.name == 'Part 1'
        p.name = None
        assert p.score_part.xml_part_name.value == p.name == 'p1'

    def test_score_part_to_string(self):
        p = Part(id='p1')
        expected = """<score-part id="p1">
  <part-name>p1</part-name>
</score-part>
"""
        assert p.score_part.to_string() == expected
