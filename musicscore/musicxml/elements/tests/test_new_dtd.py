from unittest import TestCase

from musicscore.musicxml.types.complextypes.attributes import Time, Beats, BeatType


class Test(TestCase):

    def test_dtd_time(self):
        t = Time()
        t2 = Time()
        self.assertTrue(id(t.dtd) == id(t2.dtd))
        self.assertTrue([id(node) for node in t.dtd.get_choices()] == [id(node) for node in t2.dtd.get_choices()])
        self.assertFalse(id(t.current_dtd_choice) == id(t2.current_dtd_choice))
        t2.add_child(Beats(6))
        t2.add_child(BeatType(2))
        result = '''<time>
  <beats>6</beats>
  <beat-type>2</beat-type>
</time>
'''
        self.assertEqual(t2.to_string(), result)
