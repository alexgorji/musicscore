import itertools
from unittest import TestCase

from musicxml.xmlelement.xmlelement import *

from musictree.chord import Chord
from musictree.exceptions import VoiceIsAlreadyFullError
from musictree.measure import Measure, generate_measures
from musictree.staff import Staff
from musictree.time import Time
from musictree.voice import Voice


class TestMeasure(TestCase):

    def test_measure_default_init(self):
        expected = """<measure number="1">
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
"""
        m = Measure(1)
        assert m.to_string() == expected

    def test_number(self):
        m = Measure(number=2)
        assert m.number == 2
        m.number = 4
        assert m.number == 4
        m.xml_object.number = '3'
        assert m.number == 3

    def test_measure_time_signature(self):
        m = Measure(1)
        expected = """<time>
      <beats>4</beats>
      <beat-type>4</beat-type>
    </time>
"""
        assert m.time.to_string() == expected
        m.time = Time(3, 4)
        expected = """<time>
  <beats>3</beats>
  <beat-type>4</beat-type>
</time>
"""
        assert m.time.to_string() == expected
        m = Measure(2, time=Time(5, 8, 2, 4))
        expected = """<time>
      <beats>5</beats>
      <beat-type>8</beat-type>
      <beats>2</beats>
      <beat-type>4</beat-type>
    </time>
"""
        assert m.time.to_string() == expected

    def test_measure_add_child_staff(self):
        m = Measure(1)
        assert m.get_children() == []
        st1 = m.add_child(Staff())
        assert st1.value is None
        assert m.get_children() == [st1]
        st2 = m.add_child(Staff())
        assert m.get_children() == [st1, st2]
        assert (st1.value, st2.value) == (1, 2)
        with self.assertRaises(ValueError):
            m.add_child(Staff(2))

        m = Measure(1)
        st1 = m.add_child(Staff(1))
        assert st1.value == 1

        m = Measure(1)
        with self.assertRaises(ValueError):
            m.add_child(Staff(2))

    def test_check_divisions(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v1 = st.add_child(Voice(1))
        v2 = st.add_child(Voice(2))
        quarter_durations_1 = [1 / 3, 2 / 3, 2 / 5, 3 / 5, 1, 1 / 2, 1 / 2]
        quarter_durations_2 = [1, 9 / 7, 5 / 7, 2 / 3, 1 / 3]
        for qd in quarter_durations_1:
            v1.add_chord(Chord(60, qd))
        for qd in quarter_durations_2:
            v2.add_chord(Chord(70, qd))
        m.update_divisions()
        assert m.xml_object.xml_attributes.xml_divisions.value == 210

    def test_add_chord(self):
        m = Measure(1)
        chord = Chord(60, quarter_duration=2.5)
        chord.midis[0].accidental.show = False
        m.add_chord(chord)
        m.add_chord(Chord(61, quarter_duration=1.5))
        m.update_xml_notes()
        for xml_note, duration in zip(m.find_children('XMLNote'), [4, 1, 1, 2]):
            assert xml_note.xml_duration.value == duration
        expected = """<measure number="1">
  <attributes>
    <divisions>2</divisions>
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
  <note>
    <pitch>
      <step>C</step>
      <octave>4</octave>
    </pitch>
    <duration>4</duration>
    <tie type="start" />
    <voice>1</voice>
    <type>half</type>
    <notations>
      <tied type="start" />
    </notations>
  </note>
  <note>
    <pitch>
      <step>C</step>
      <octave>4</octave>
    </pitch>
    <duration>1</duration>
    <tie type="stop" />
    <voice>1</voice>
    <type>eighth</type>
    <notations>
      <tied type="stop" />
    </notations>
  </note>
  <note>
    <pitch>
      <step>C</step>
      <alter>1</alter>
      <octave>4</octave>
    </pitch>
    <duration>1</duration>
    <tie type="start" />
    <voice>1</voice>
    <type>eighth</type>
    <accidental>sharp</accidental>
    <notations>
      <tied type="start" />
    </notations>
  </note>
  <note>
    <pitch>
      <step>C</step>
      <alter>1</alter>
      <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <tie type="stop" />
    <voice>1</voice>
    <type>quarter</type>
    <notations>
      <tied type="stop" />
    </notations>
  </note>
</measure>
"""
        assert m.to_string() == expected

    def test_get_staff(self):
        m = Measure(1)
        assert m.get_staff(staff=None) is None
        st = m.add_child(Staff())
        assert m.get_staff(staff=None) == st
        st.value = 1
        assert m.get_staff(staff=1) == st
        st = m.add_child(Staff())
        assert m.get_staff(staff=2) == st

    def test_add_staff(self):
        m = Measure(1)
        st = m.add_staff()
        assert m.get_staff(staff=None) == st

        st = m.add_staff()
        assert st.value is None

        st = m.add_staff(1)
        assert m.get_staff(staff=1) == st

        st = m.add_staff(5)
        assert m.get_staff(staff=5) == st
        assert len(m.get_children()) == 5
        assert [st.value for st in m.get_children()] == [1, 2, 3, 4, 5]

    def test_add_voice(self):
        m = Measure(1)
        v = m.add_voice(staff=None, voice=2)
        st = m.get_staff(staff=None)
        assert st.get_children()[-1] == v
        assert [v.value for v in st.get_children()] == [1, 2]

        v = m.add_voice(staff=2, voice=3)
        assert [st.value for st in m.get_children()] == [1, 2]
        assert [v.value for v in m.get_staff(2).get_children()] == [1, 2, 3]

    def test_get_voice(self):
        m = Measure(1)
        with self.assertRaises(TypeError):
            m.get_voice(None, 1)
        assert m.get_voice(staff=None, voice=1) is None
        st = m.add_child(Staff())
        assert m.get_voice(staff=None, voice=1) is None
        v = st.add_child(Voice())
        assert m.get_voice(staff=None, voice=1) == v
        assert m.get_voice(staff=1, voice=1) == v
        v = st.add_child(Voice())
        assert m.get_voice(staff=None, voice=2) == v

    def test_add_chord_voice_filled(self):
        m = Measure(1)
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m.add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 2
        assert m.get_children()[0].get_children()[0].left_over_chord is None
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m.add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 2
        assert m.get_children()[0].get_children()[0].left_over_chord is None
        with self.assertRaises(VoiceIsAlreadyFullError):
            m.add_chord(Chord(quarter_duration=2, midis=60))
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m.add_chord(ch, voice=2)
        assert len(returned_chords) == 1
        assert [ch.voice for ch in m.get_chords()] == [1, 1, 2]

    def test_add_chord_left_over(self):
        m = Measure(1)
        ch = Chord(quarter_duration=5, midis=60)
        returned_chords = m.add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 4
        assert m.get_voice(staff=1, voice=1).left_over_chord.quarter_duration == 1

    def test_attributes(self):
        """
        Test that a dot operator can directly reach the xml_object
        """
        m = Measure(1)
        m.xml_object.width = 5
        assert m.width == 5

        m.width = 7
        assert m.xml_object.width == 7

        with self.assertRaises(AttributeError):
            m.hello = 'bbb'
        m.xml_object.width = 10
        assert m.xml_object.width == 10
        assert m.width == 10

        m = Measure(1)
        m.width = 10
        assert m.width == 10
        assert m.xml_object.width == 10

    def test_barstyle(self):
        m = Measure(number='1')
        assert m.xml_barline is None
        m.xml_barline = XMLBarline()
        m.xml_barline.xml_bar_style = 'light-light'
        expected = """<measure number="1">
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
  <barline>
    <bar-style>light-light</bar-style>
  </barline>
</measure>
"""
        assert m.xml_object.to_string() == expected

    def test_update_beats_from_parent_measure(self):
        v = Voice()
        m = Measure(1)
        st = m.add_child(Staff())
        st.add_child(v)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 4

        m = Measure(1, time=Time(3, 4, 1, 8))
        st = m.add_child(Staff())
        st.add_child(v)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 3 + [(1, 2)]

        m.time = Time(2, 8)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 2)] * 2

        m.time.signatures = [3, 4, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 3 + [(1, 2)]

        m.time.actual_signatures = [1, 8, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 2)] * 2

    def test_generate_measures(self):
        # times = [2 * (1, 4), 3 * (1, 8), Time(1, 8, 3, 4), Time(3, 4, actual_signatures=(1, 8, 2, 4, 1, 8))]
        times = [2 * Time(3, 8), (3, 4), 3 * [(1, 8)], Time(1, 8, 3, 4), Time(3, 4)]
        measures = generate_measures(times, 3)
        assert len(measures) == 8
        assert [m.time.signatures for m in measures] == [(3, 8), (3, 8), (3, 4), (1, 8), (1, 8), (1, 8), (1, 8, 3, 4), (3, 4)]
        assert [m.number for m in measures] == list(range(3, 11))

    def test_add_chord_staff_and_voice(self):
        m = Measure(1)
        m.add_chord(Chord(60, 1), staff=2, voice=2)
        assert m.get_staff(2) is not None
        assert m.get_voice(staff=2, voice=2) is not None
        m.add_chord(Chord(60, 1), staff=4, voice=5)
        assert m.get_voice(staff=3, voice=1) is not None
        assert m.get_voice(staff=3, voice=2) is None
        assert m.get_voice(staff=3, voice=5) is None
        assert m.get_voice(staff=4, voice=1) is not None
        assert m.get_voice(staff=4, voice=2) is not None
        assert m.get_voice(staff=4, voice=3) is not None
        assert m.get_voice(staff=4, voice=4) is not None
        assert m.get_voice(staff=4, voice=5) is not None
