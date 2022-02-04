from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.tests.util import IdTestCase


class TestScore(IdTestCase):
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
        <measure number="1">
            <attributes>
                <divisions>1</divisions>
                <key>
                    <fifths>0</fifths>
                </key>
                <time>
                    <beats>4</beats>
                    <beat-type>4</beat-type>
                </time>
                <clef>
                    <sign>G</sign>
                    <line>2</line>
                </clef>
            </attributes>
        </measure>
    </part>
</score-partwise>
"""
        assert s.to_string() == expected

    def test_get_chords(self):
        s = Score()
        p = s.add_child(Part('p1'))
        m = p.add_child(Measure(1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        m.add_chord(Chord(midis=60, quarter_duration=1))
        assert len(s.get_chords()) == 4
        assert type(s.get_chords()[0]) == Chord
