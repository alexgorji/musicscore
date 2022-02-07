from unittest import TestCase
from unittest.mock import patch

from musictree.measure import Measure
from musictree.staff import Staff
from musictree.voice import Voice


class TestStaff(TestCase):
    def test_staff_init(self):
        st = Staff()
        assert st.value is None
        assert st.xml_object.value is None
        st = Staff(3)
        assert st.xml_object.value == 3
        assert st.value == 3
        st.value = 2
        assert st.xml_object.value == 2
        st.xml_object.value = None
        assert st.value is None
        assert st.xml_object.value is None

    @patch('musictree.measure.Measure')
    def test_add_child(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        assert [child.value for child in st.get_children()] == []
        st.add_child(Voice())
        assert [child.value for child in st.get_children()] == [1]
        st.add_child(Voice())
        assert len(st.get_children()) == 2
        assert [child.value for child in st.get_children()] == [1, 2]

    @patch('musictree.measure.Measure')
    def test_add_voice(self, mock_measure):
        st = Staff()
        st._parent = mock_measure
        v = st.add_voice()
        assert st.get_children()[-1] == v
        assert len(st.get_children()) == 1
        assert v.value == 1
        v = st.add_voice(4)
        assert v.value == 4
        assert len(st.get_children()) == 4
        assert [v.value for v in st.get_children()] == [1, 2, 3, 4]
