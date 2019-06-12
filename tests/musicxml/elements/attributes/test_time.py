from unittest import TestCase

from musicscore.musicxml.types.complextypes.attributes import Time, Beats, BeatType, SenzaMisura


class TestTime(TestCase):

    def setUp(self):
        self.time = Time()
        self.time.add_child(Beats(3))
        self.time.add_child(BeatType(2))

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

    def test_senza_misura(self):
        with self.assertRaises(NotImplementedError):
            self.time.add_child(SenzaMisura())

    def test_multiple_time_signatures(self):
        time = Time()
        time.add_child(Beats(3))
        time.add_child(BeatType(4))
        time.add_child(Beats(1))
        time.add_child(BeatType(8))
        result = '''<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
  <beats>1</beats>
  <beat-type>8</beat-type>
</time>
'''
        self.assertEqual(time.to_string(), result)
