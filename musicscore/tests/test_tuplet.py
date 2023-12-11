from unittest import TestCase

from musicscore.exceptions import TupletNormalTypeError
from musicscore.tuplet import Tuplet
from musicxml import XMLTimeModification


class TestTuplet(TestCase):
    def test_init(self):
        t = Tuplet(actual_notes=3, normal_notes=2, normal_type='eighth', bracket_type='start', bracket_number=1)
        assert t.actual_notes == 3
        assert t.normal_notes == 2
        assert t.normal_type == 'eighth'
        assert t.bracket_type == 'start'
        assert t.bracket_number == 1

    def test_property_exceptions(self):
        t = Tuplet()
        with self.assertRaises(ValueError):
            t.actual_notes = -1
        with self.assertRaises(ValueError):
            t.actual_notes = 0
        with self.assertRaises(ValueError):
            t.actual_notes = 1
        with self.assertRaises(TypeError):
            t.actual_notes = None
        with self.assertRaises(TypeError):
            t.actual_notes = '1'

        with self.assertRaises(ValueError):
            t.normal_notes = -1
        with self.assertRaises(ValueError):
            t.normal_notes = 0
        with self.assertRaises(ValueError):
            t.normal_notes = 1

        with self.assertRaises(TypeError):
            t.normal_notes = '1'

        with self.assertRaises(ValueError):
            t.normal_type = 'bla'

        with self.assertRaises(ValueError):
            t.bracket_type = 'bla'

        with self.assertRaises(ValueError):
            t.bracket_number = -1
        with self.assertRaises(ValueError):
            t.bracket_number = 0
        with self.assertRaises(TypeError):
            t.bracket_number = '1'

    def test_default_values(self):
        t = Tuplet()
        assert t.actual_notes == 3
        assert t.normal_notes == 2
        assert t.normal_type == 'eighth'
        assert t.bracket_type is None
        assert t.bracket_number is None

    def test_tuplet_get_xml_time_modification(self):
        t = Tuplet()
        tm = t.get_xml_time_modification()
        assert isinstance(tm, XMLTimeModification)
        assert tm.xml_actual_notes.value_ == t.actual_notes
        assert tm.xml_normal_notes.value_ == t.normal_notes
        assert tm.xml_normal_type.value_ == t.normal_type

    def test_tuplet_get_xml_tuplet(self):
        t = Tuplet()
        assert t.get_xml_tuplet() is None
        assert t.bracket_number is None
        t.bracket_type = 'start'
        assert t.bracket_number == 1
        assert t.get_xml_tuplet().bracket == 'yes'
        assert t.get_xml_tuplet().type == t.bracket_type
        assert t.get_xml_tuplet().number == 1
        t.bracket_number = 2
        assert t.bracket_number == 2
        assert t.get_xml_tuplet().number == 2

    def test_tuplet_quarter_duration(self):
        t = Tuplet()
        assert t.quarter_duration == 1
        t.quarter_duration = 1.2
        with self.assertRaises(TupletNormalTypeError):
            t.normal_type

    def test_tuplet_automatic_type(self):
        t = Tuplet(quarter_duration=2)
        assert t.normal_type == 'quarter'
        t.quarter_duration = 1 / 2
        assert t.normal_type == '16th'
