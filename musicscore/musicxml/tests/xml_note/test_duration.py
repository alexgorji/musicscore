from unittest import TestCase
from musicscore.musicxml.elements.note import Duration


class TestDuration(TestCase):
    def setUp(self):
        self.duration = Duration(10)

    def test_duration(self):
        result = '''<duration>10</duration>
'''
        self.assertEqual(self.duration.to_string(), result)
        self.duration.value = 2
        result = '''<duration>2</duration>
'''
        self.duration.text = 3
        result = '''<duration>3</duration>
'''
        self.assertEqual(self.duration.to_string(), result)
