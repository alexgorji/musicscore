from unittest import TestCase
from musicscore.musicxml.elements.attributes import Time


class TestTime(TestCase):

    def setUp(self):
        self.time = Time(3, 2)

    def test_time(self):
        result = '''<time>
  <beats>3</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)

    def test_print(self):
        self.time.print_object = 'no'
        result = '''<time print-object="no">
  <beats>3</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)

        self.time.print_object = None
        result = '''<time>
  <beats>3</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)

        self.time.print_object = 'yes'
        result = '''<time print-object="yes">
  <beats>3</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(self.time.to_string(), result)
        with self.assertRaises(ValueError):
            self.time.print_object = 'bla'
