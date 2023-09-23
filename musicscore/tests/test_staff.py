from unittest import TestCase
from unittest.mock import patch

from musicscore.chord import Chord
from musicscore.measure import Measure
from musicscore.part import Part
from musicscore.staff import Staff
from musicscore.voice import Voice
from musicxml import XMLVoice, XMLStaff


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

    @patch('musicscore.measure.Measure')
    def test_add_child(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        assert [child.number for child in st.get_children()] == []
        st.add_child(Voice())
        assert [child.number for child in st.get_children()] == [1]
        st.add_child(Voice())
        assert len(st.get_children()) == 2
        assert [child.number for child in st.get_children()] == [1, 2]

    @patch('musicscore.measure.Measure')
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
        m1._add_chord(Chord(midis=[61, 62, 63], quarter_duration=2))
        m1._add_chord(Chord(midis=[63, 64, 66], quarter_duration=2))
        assert m1.get_staff(1).get_last_pitch_steps_with_accidentals() == {'E', 'F'}

    def test_staff_clef(self):
        st = Staff()
        assert st.clef is None

    def test_get_staff_number_from_midi(self):
        part = Part('p1')
        ch = Chord([60, 70, 80], 2)
        part.add_chord(ch)
        ch.midis[0].set_staff_number(2)
        ch.midis[1].set_staff_number(2)
        part.finalize()

        for index, n in enumerate(ch.notes):
            if index in [0, 1]:
                assert n.xml_object.xml_staff.value_ == 2
            else:
                assert not n.xml_object.xml_staff
