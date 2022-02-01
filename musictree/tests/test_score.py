from unittest import TestCase

from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score


class TestScore(TestCase):
    def test_score_version(self):
        s = Score(version=3.1)
        assert s.version == '3.1'
        s = Score()
        assert s.version == '4.0'

    def test_score_init(self):
        s = Score()
        p = s.add_child(Part('p1'))
        p.add_child(Measure(1))
        assert s.xml_part_list.find_child('XMLScorePart') == p.score_part.xml_object

        expected = """<score-partwise version="4.0">
    <part-list>
        <score-part id="p1">
            <part-name>p1</part-name>
        </score-part>
    </part-list>
    <part id="p1">
        <measure number="1" />
    </part>
</score-partwise>
"""
        assert s.to_string() == expected
