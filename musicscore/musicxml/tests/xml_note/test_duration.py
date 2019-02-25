from unittest import TestCase
from musicscore.musicxml.elements.xml_note import XMLDuration


class TestDuration(TestCase):
    def setUp(self):
        self.duration = XMLDuration(10)

    def test_duration(self):
        result = '''<duration>10</duration>
'''
        self.assertEqual(self.duration.to_string(), result)
        self.duration.value = 2
        result = '''<duration>2</duration>
'''
        with self.assertWarns(Warning):
            self.assertEqual(self.duration.to_string(), result)
