from unittest import TestCase
from musicscore.timewise import Timwise


class TestTimewise(TestCase):
    def setUp(self):
        self.timewise = Timwise()

    def test_add_part(self):
        self.timewise.add_part()
        self.timewise.add_part(print_object='yes', name='oboe')
        resutl = '''<score-timewise>
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">none</part-name>
    </score-part>
    <score-part id="p2">
      <part-name print-object="yes">oboe</part-name>
    </score-part>
  </part-list>
</score-timewise>
'''
        self.assertEqual(self.timewise.to_string(), resutl)

    def test_add_measure_part(self):
        self.timewise.add_measure()
        self.timewise.add_part()
        print(self.timewise.to_string())
