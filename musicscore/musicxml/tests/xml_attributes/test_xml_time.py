from unittest import TestCase
from musicscore.musicxml.elements.xml_attributes import XMLTime


class TestTime(TestCase):
    def setUp(self):
        self.time = XMLTime(4,7)

    def test_time(self):
        result = '''<time>
  <beats>4</beats>
  <beat-type>7</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)
