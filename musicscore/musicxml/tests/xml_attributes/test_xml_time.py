from unittest import TestCase
from musicscore.musicxml.elements.xml_attributes import XMLTime


class TestTime(TestCase):

    def setUp(self):
        self.time = XMLTime(3, 2)

    def test_time(self):
        result = '''<time>
  <beats>3</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)

    def test_print(self):
        self.time.print_object = 'no'
        print(self.time.to_string())
        self.time.print_object = None
        print(self.time.to_string())
        self.time.print_object = 'yes'
        print(self.time.to_string())
        with self.assertRaises(ValueError):
            self.time.print_object = 'bla'
