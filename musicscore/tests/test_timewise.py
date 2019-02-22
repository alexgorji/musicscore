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
        self.timewise.add_part()
        self.timewise.add_measure()
        result = '''<score-timewise>
  <part-list>
    <score-part id="p1">
      <part-name print-object="no">none</part-name>
    </score-part>
    <score-part id="p2">
      <part-name print-object="no">none</part-name>
    </score-part>
  </part-list>
  <measure number="1">
    <part id="p1"/>
    <part id="p2"/>
  </measure>
  <measure number="2">
    <part id="p1"/>
    <part id="p2"/>
  </measure>
</score-timewise>
'''
        self.assertEqual(self.timewise.to_string(), result)
