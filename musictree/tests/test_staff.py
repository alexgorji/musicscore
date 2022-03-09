from unittest import TestCase
from unittest.mock import patch

from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.staff import Staff
from musictree.voice import Voice


class TestStaff(TestCase):
    def test_staff_init(self):
        st = Staff()
        assert st.number is None
        assert st.xml_object.value_ == 1
        st = Staff(number=3)
        assert st.xml_object.value_ == 3
        assert st.number == 3
        st.number = 2
        assert st.xml_object.value_ == 2
        st.xml_object.value_ = 1
        assert st.number is 1
        assert st.xml_object.value_ == 1

    @patch('musictree.measure.Measure')
    def test_add_child(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        assert [child.number for child in st.get_children()] == []
        st.add_child(Voice())
        assert [child.number for child in st.get_children()] == [1]
        st.add_child(Voice())
        assert len(st.get_children()) == 2
        assert [child.number for child in st.get_children()] == [1, 2]

    @patch('musictree.measure.Measure')
    def test_add_voice(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_voice()
        assert st.get_children()[-1] == v
        assert len(st.get_children()) == 1
        assert v.number == 1
        v = st.add_voice()
        assert st.get_children()[-1] == v
        assert len(st.get_children()) == 2
        assert v.number == 2

        v = st.add_voice(5)
        assert v.number == 5
        assert len(st.get_children()) == 5
        assert [v.number for v in st.get_children()] == [1, 2, 3, 4, 5]

    def test_get_previous_staff(self):
        p = Part('P1')
        m1 = p.add_measure()
        m2 = p.add_measure()
        m1.add_staff(2)
        m2.add_staff(2)
        st11, st12 = m1.get_children()
        st21, st22 = m2.get_children()
        assert st11.get_previous_staff() is None
        assert st12.get_previous_staff() is None
        assert st21.get_previous_staff() == st11
        assert st22.get_previous_staff() == st12

    def test_get_last_steps_with_accidentals(self):
        m1 = Measure(1)
        m1.add_chord(Chord(midis=[61, 62, 63], quarter_duration=2))
        m1.add_chord(Chord(midis=[63, 64, 66], quarter_duration=2))
        assert m1.get_staff(1).get_last_pitch_steps_with_accidentals() == {'E', 'F'}

    @patch('musictree.measure.Measure')
    def test_staff_clef(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        assert st.clef.sign == 'G'
        assert st.clef.line == 2
