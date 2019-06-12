from unittest import TestCase

from musicscore.musicxml.types.complextypes.attributes import Divisions


class TestDivisions(TestCase):

    def setUp(self):
        self.divisions = Divisions(1)

    def test_divisions(self):
        result = '''<divisions>1</divisions>
'''
        self.assertEqual(self.divisions.to_string(), result)
        self.divisions.value = 2
        result = '''<divisions>2</divisions>
'''
        self.assertEqual(self.divisions.to_string(), result)

        self.divisions.text = 3
        result = '''<divisions>3</divisions>
'''
        self.assertEqual(self.divisions.to_string(), result)

