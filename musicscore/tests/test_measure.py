from unittest import TestCase, skip

from musicscore import Score
from musicscore.chord import Chord
from musicscore.clef import BassClef, TrebleClef
from musicscore.exceptions import VoiceIsFullError, AddChordError
from musicscore.measure import Measure, generate_measures
from musicscore.part import Part
from musicscore.staff import Staff
from musicscore.tests.util import IdTestCase
from musicscore.time import Time
from musicscore.voice import Voice
from musicxml.xmlelement.xmlelement import *


class TestMeasure(IdTestCase):
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
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
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
        assert st1.number is None
        assert m.get_children() == [st1]
        st2 = m.add_child(Staff())
        assert m.get_children() == [st1, st2]
        assert (st1.number, st2.number) == (1, 2)
        with self.assertRaises(ValueError):
            m.add_child(Staff(number=2))

        m = Measure(1)
        st1 = m.add_child(Staff(number=1))
        assert st1.number == 1

        m = Measure(1)
        with self.assertRaises(ValueError):
            m.add_child(Staff(number=2))

    def test_check_divisions(self):
        m = Measure(1)
        st = m.add_child(Staff())
        v1 = st.add_child(Voice(1))
        v2 = st.add_child(Voice(2))
        v1.update_beats()
        v2.update_beats()
        quarter_durations_1 = [1 / 3, 2 / 3, 2 / 5, 3 / 5, 1, 1 / 2, 1 / 2]
        quarter_durations_2 = [1, 9 / 7, 5 / 7, 2 / 3, 1 / 3]
        for qd in quarter_durations_1:
            v1._add_chord(Chord(60, qd))
        for qd in quarter_durations_2:
            v2._add_chord(Chord(70, qd))
        m._update_divisions()
        assert m.xml_object.xml_attributes.xml_divisions.value_ == 210

    def test_add_chord(self):
        m = Measure(1)
        chord = Chord(60, quarter_duration=2.5)
        chord.midis[0].accidental.show = False
        m._add_chord(chord)
        chord = Chord(61, quarter_duration=1.5)
        chord.midis[0].accidental.show = True
        m._add_chord(chord)
        m.finalize()
        for xml_note, duration in zip(m.find_children('XMLNote'), [4, 1, 1, 2]):
            assert xml_note.xml_duration.value_ == duration
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
    <beam number="1">begin</beam>
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
    <beam number="1">end</beam>
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
        assert m.get_staff(staff_number=1) is None
        st = m.add_child(Staff())
        assert m.get_staff(staff_number=1) == st
        st.number = 1
        assert m.get_staff(staff_number=1) == st
        st = m.add_child(Staff())
        assert m.get_staff(staff_number=2) == st

    def test_add_staff(self):
        m = Measure(1)
        st1 = m.add_staff()
        assert m.get_children()[0] == st1
        assert m.get_staff(1) == st1
        assert st1.number is None

        st2 = m.add_staff()
        assert st1.number == 1
        assert st2.number == 2
        st3 = m.add_staff()
        assert st3.number == 3
        # print(m.get_children())

        m = Measure(1)
        st = m.add_staff()
        assert st.number is None
        assert m.get_staff(staff_number=1) == st

        st = m.add_staff(1)
        assert m.get_staff(staff_number=1) == st

        st = m.add_staff(5)
        assert m.get_staff(staff_number=5) == st
        assert len(m.get_children()) == 5
        assert [st.number for st in m.get_children()] == [1, 2, 3, 4, 5]

    def test_add_voice(self):
        m = Measure(1)
        v = m.add_voice(staff_number=None, voice_number=2)
        st = m.get_staff(staff_number=1)
        assert st.get_children()[-1] == v
        assert [v.number for v in st.get_children()] == [1, 2]

        m.add_voice(staff_number=2, voice_number=3)
        assert [st.number for st in m.get_children()] == [1, 2]
        assert [v.number for v in m.get_staff(2).get_children()] == [1, 2, 3]

        m = Measure(1)
        m.add_voice(staff_number=2, voice_number=2)
        st1, st2 = m.get_children()
        assert len(st2.get_children()) == 2
        assert len(st1.get_children()) == 1

    def test_get_voice(self):
        m = Measure(1)
        with self.assertRaises(TypeError):
            m.get_voice(None, 1)
        assert m.get_voice(staff_number=1, voice_number=1) is None
        st = m.add_child(Staff())
        assert m.get_voice(staff_number=1, voice_number=1) is None
        v = st.add_child(Voice())
        assert m.get_voice(staff_number=1, voice_number=1) == v
        assert m.get_voice(staff_number=1, voice_number=1) == v
        v = st.add_child(Voice())
        assert m.get_voice(staff_number=1, voice_number=2) == v

    def test_add_chord_voice_filled(self):
        m = Measure(1)
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m._add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 2
        assert m.get_children()[0].get_children()[0].leftover_chord is None
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m._add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 2
        assert m.get_children()[0].get_children()[0].leftover_chord is None
        with self.assertRaises(VoiceIsFullError):
            m._add_chord(Chord(quarter_duration=2, midis=60))
        ch = Chord(quarter_duration=2, midis=60)
        returned_chords = m._add_chord(ch, voice_number=2)
        assert len(returned_chords) == 1
        assert [ch.voice_number for ch in m.get_chords()] == [1, 1, 2]

    def test_add_chord_leftover(self):
        m = Measure(1)
        ch = Chord(quarter_duration=5, midis=60)
        returned_chords = m._add_chord(ch)
        assert len(returned_chords) == 1
        assert returned_chords[0] == ch
        assert returned_chords[0].quarter_duration == 4
        assert m.get_voice(staff_number=1, voice_number=1).leftover_chord.quarter_duration == 1

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

    def test_left_and_right_barline_property(self):
        m = Measure(number='1')
        assert m.get_barline(location='left') == m.get_barline() == m.get_barline(location='right') is None

        m.set_barline(location='left')
        assert isinstance(m.get_barline(location='left'), XMLBarline)
        assert not m.get_barline(location='left').get_children()

        m.set_barline(location='right')
        assert isinstance(m.get_barline(location='right'), XMLBarline)
        assert not m.get_barline(location='right').get_children()
        assert isinstance(m.get_barline(), XMLBarline)
        assert not m.get_barline().get_children()

        barline_styles = ['regular', 'regular', 'dotted', 'dashed', 'heavy', 'light-light', 'light-heavy',
                          'heavy-light', 'heavy-heavy', 'tick', 'short', 'none']
        for bs in barline_styles:
            m = Measure(1)
            m.set_barline(style=bs)
            m.finalize()
            assert m.xml_barline.xml_bar_style.value_ == bs
            assert m.xml_barline.location == 'right'

        for bs in barline_styles:
            m = Measure(1)
            m.set_barline(style=bs, location='left')
            m.finalize()
            assert m.xml_barline.xml_bar_style.value_ == bs
            assert m.xml_barline.location == 'left'

    def test_barline(self):
        m = Measure(number='1')
        m.set_barline(style='light-light')
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
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
  <barline location="right">
    <bar-style>light-light</bar-style>
  </barline>
</measure>
"""
        assert m.to_string() == expected

    def test_update_beats_from_parent_measure(self):
        v = Voice()
        m = Measure(1)
        st = m.add_child(Staff())
        st.add_child(v)
        v.update_beats()
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 4

        m = Measure(1, time=Time(3, 4, 1, 8))
        st = m.add_child(Staff())
        st.add_child(v)
        v.update_beats()
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 3 + [(1, 2)]

        m.time = Time(2, 8)
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)]

        m.time.signatures = [3, 4, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 1)] * 3 + [(1, 2)]

        m.time.actual_signatures = [1, 8, 1, 8]
        assert [child.quarter_duration.as_integer_ratio() for child in v.get_children()] == [(1, 2)] * 2

    def test_generate_measures(self):
        times = [2 * Time(3, 8), (3, 4), 3 * [(1, 8)], Time(1, 8, 3, 4), Time(3, 4)]
        measures = generate_measures(times, 3)
        assert len(measures) == 8
        assert [m.time.signatures for m in measures] == [(3, 8), (3, 8), (3, 4), (1, 8), (1, 8), (1, 8), (1, 8, 3, 4),
                                                         (3, 4)]
        assert [m.number for m in measures] == list(range(3, 11))

    def test_add_chord_staff_and_voice(self):
        m = Measure(1)
        m._add_chord(Chord(60, 1), staff_number=2, voice_number=2)
        assert m.get_staff(2) is not None
        assert m.get_voice(staff_number=2, voice_number=2) is not None
        m._add_chord(Chord(60, 1), staff_number=4, voice_number=5)
        assert m.get_voice(staff_number=3, voice_number=1) is not None
        assert m.get_voice(staff_number=3, voice_number=2) is None
        assert m.get_voice(staff_number=3, voice_number=5) is None
        assert m.get_voice(staff_number=4, voice_number=1) is not None
        assert m.get_voice(staff_number=4, voice_number=2) is not None
        assert m.get_voice(staff_number=4, voice_number=3) is not None
        assert m.get_voice(staff_number=4, voice_number=4) is not None
        assert m.get_voice(staff_number=4, voice_number=5) is not None

    def test_update_dynamics(self):
        m = Measure(1)
        chord = Chord(60, quarter_duration=2.5)
        chord.add_dynamics(["ppp", 'fff'])
        m._add_chord(chord)
        m.finalize()
        assert m.xml_direction is not None
        expected = """<direction placement="below">
    <direction-type>
      <dynamics>
        <ppp />
      </dynamics>
    </direction-type>
    <direction-type>
      <dynamics>
        <fff />
      </dynamics>
    </direction-type>
  </direction>
"""

        assert m.xml_direction.to_string() == expected

    def test_add_chord_to_measure(self):
        part = Part(id='part-1')
        measure = part.add_measure(time=Time(4, 4))
        with self.assertRaises(AddChordError):
            measure.add_chord(Chord(midis=60, quarter_duration=15))

    def test_default_staff(self):
        # inconsistency add_part doesn't add measure but add_measure does create staff, voice and beats
        m = Measure(1)
        assert len(m.get_children()) == 0
        score = Score()
        p = score.add_part('p1')
        assert len(m.get_children()) == 0
        m = p.add_measure()
        assert len(m.get_children()) == 1
        assert len(m.get_children()[0].get_children()) == 1
        v = m.get_children()[0].get_children()[0]
        assert len(v.get_children()) == 4

    def test_new_system(self):
        s = Score()
        p = s.add_part('part1')
        p.add_chord(Chord(quarter_duration=4 * 4 * 4, midis=60))
        m = p.get_measure(1)
        assert m.new_system is False
        m.new_system = True
        assert m.new_system is True
        assert m.xml_object.xml_print.new_system == 'yes'
        s.finalize()
        s.xml_object._final_checks()

    def test_add_repeat_left(self):
        m = Measure(1)
        m._add_chord(Chord(60, 4))
        m.set_repeat_barline(times=5)
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
  <note>
    <pitch>
      <step>C</step>
      <octave>4</octave>
    </pitch>
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
  <barline location="right">
    <bar-style>light-heavy</bar-style>
    <repeat direction="backward" times="5" />
  </barline>
</measure>
"""
        assert m.to_string() == expected

    def test_add_ending_without_repeat(self):
        m = Measure(1)
        # add_ending needs number and type
        with self.assertRaises(TypeError):
            m.set_repeat_ending()
        with self.assertRaises(TypeError):
            m.set_repeat_ending(number=1)
        with self.assertRaises(TypeError):
            m.set_repeat_ending(type='stop')
        # wrong type
        with self.assertRaises(ValueError):
            m.set_repeat_ending(number=1, type='bal')

        # right init
        m._add_chord(Chord(0, 4))
        m.set_repeat_ending(number=2, type='discontinue')
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
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
  <barline location="right">
    <ending number="2" type="discontinue" />
  </barline>
</measure>
"""
        assert m.to_string() == expected

    def test_measure_fill_with_rests(self):
        m = Measure(1)
        m.fill_with_rests()
        ch = m.get_chords()[0]
        assert ch.is_rest
        assert ch.quarter_duration == 4


class TestUpdateAccidentals(IdTestCase):
    def test_update_accidentals_simple(self):
        m = Measure(1)
        midis = [60, 61, 62, 60]
        for mi in midis:
            m._add_chord(Chord(mi, quarter_duration=1))
        m.finalize()
        assert [ch.midis[0].accidental.show for ch in m.get_chords()] == [False, True, False, True]

    def test_update_accidentals_with_last_steps(self):
        p = Part('P1')
        p.add_measure()
        p.add_measure()
        p.add_chord(Chord(midis=60, quarter_duration=2))
        p.add_chord(Chord(midis=61, quarter_duration=2))
        p.add_chord(Chord(midis=60, quarter_duration=4))
        for m in p.get_children():
            m.finalize()
        last_chord = p.get_children()[-1].get_children()[-1].get_chords()[0]
        assert last_chord.midis[0].accidental.sign == 'natural'
        assert last_chord.midis[0].accidental.show

    def test_quarter_duration(self):
        m = Measure(1)
        assert m.quarter_duration == 4
        m.time.signatures = (3, 4)
        assert m.quarter_duration == 3
        m.time.signatures = (2, 4, 1, 8)
        assert m.quarter_duration == 2.5

    def test_xml_notes_with_different_voices(self):
        m = Measure(1)
        m._add_chord(Chord(60, 4))
        m._add_chord(Chord(60, 4), voice_number=2)
        m.finalize()
        ch1, ch2 = m.get_chords()
        assert ch1.notes[0].xml_voice.value_ == '1'
        assert ch2.notes[0].xml_voice.value_ == '2'
        b = m.xml_object.find_child('XMLBackup')
        assert b is not None

    def test_xml_notes_with_different_staves(self):
        m = Measure(1)
        m._add_chord(Chord(72, 4), staff_number=1, voice_number=1)
        m._add_chord(Chord(60, 4), staff_number=1, voice_number=2)
        m._add_chord(Chord(48, 4), staff_number=2, voice_number=1)
        m._add_chord(Chord(36, 4), staff_number=2, voice_number=2)
        m.clefs[1] = BassClef()
        m.finalize()
        ch1, ch2, ch3, ch4 = m.get_chords()
        assert ch1.notes[0].xml_staff.value_ == 1
        assert ch2.notes[0].xml_staff.value_ == 1
        assert ch3.notes[0].xml_staff.value_ == 2
        assert ch4.notes[0].xml_staff.value_ == 2
        assert ch1.notes[0].xml_voice.value_ == '1'
        assert ch2.notes[0].xml_voice.value_ == '2'
        assert ch3.notes[0].xml_voice.value_ == '1'
        assert ch4.notes[0].xml_voice.value_ == '2'
        backups = m.xml_object.find_children('XMLBackup')
        assert len(backups) == 3
        assert m.xml_attributes.xml_staves.value_ == 2

        cl1, cl2 = m.xml_attributes.find_children('XMLClef')
        assert cl1.number == 1
        assert cl2.number == 2
        assert cl1.xml_sign.value_ == 'G'
        assert cl1.xml_line.value_ == 2
        assert cl2.xml_sign.value_ == 'F'
        assert cl2.xml_line.value_ == 4

    @skip
    def test_update_chord_accidentals(self):
        self.fail()


class TestMeasureAttributes(TestCase):
    def test_measure_update_attributes(self):
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
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</measure>
"""
        m = Measure(1)
        m.add_staff()
        m._update_attributes()
        assert m.to_string() == expected

    def test_measure_clefs(self):
        m = Measure(1)
        m.add_staff()
        m.finalize()
        clefs = m.xml_object.xml_attributes.find_children('XMLClef')
        assert clefs[0].xml_sign.value_ == 'G'
        assert clefs[0].xml_line.value_ == 2

        m = Measure(1)
        m.add_staff()
        m.add_staff()
        m.finalize()
        clefs = m.xml_object.xml_attributes.find_children('XMLClef')
        assert clefs[0].xml_sign.value_ == 'G'
        assert clefs[0].xml_line.value_ == 2
        assert clefs[1].xml_sign.value_ == 'F'
        assert clefs[1].xml_line.value_ == 4

        m = Measure(1)
        m.add_staff()
        m.add_staff()
        m.finalize()
        m.clefs[0].sign = 'C'
        m.clefs[0].line = 3

        clefs = m.xml_object.xml_attributes.find_children('XMLClef')
        assert clefs[0].xml_sign.value_ == 'C'
        assert clefs[0].xml_line.value_ == 3

    def test_measure_add_staff_clef(self):
        m = Measure(1)
        assert not m.clefs
        m.add_staff()
        assert len(m.clefs) == 1
        assert m.clefs[0].number is None
        m.clefs[0].sign = 'G'
        m.clefs[0].line = 2

        m.add_staff()
        assert len(m.clefs) == 2
        assert [cl.number for cl in m.clefs] == [1, 2]
        assert [cl.sign for cl in m.clefs] == ['G', 'F']
        assert [cl.line for cl in m.clefs] == [2, 4]

        m.add_staff()
        assert len(m.clefs) == 3
        assert [cl.number for cl in m.clefs] == [1, 2, 3]
        assert [cl.sign for cl in m.clefs] == ['G', 'G', 'F']
        assert [cl.line for cl in m.clefs] == [2, 2, 4]
        assert [cl.octave_change for cl in m.clefs] == [2, None, None]

        m.add_staff()
        assert len(m.clefs) == 4
        assert [cl.number for cl in m.clefs] == [1, 2, 3, 4]
        assert [cl.sign for cl in m.clefs] == ['G', 'G', 'F', 'F']
        assert [cl.line for cl in m.clefs] == [2, 2, 4, 4]
        assert [cl.octave_change for cl in m.clefs] == [2, None, None, -2]

        m.add_staff()
        assert len(m.clefs) == 5
        assert [cl.number for cl in m.clefs] == [1, 2, 3, 4, 5]
        assert [cl.sign for cl in m.clefs] == ['G', 'G', 'G', 'F', 'F']
        assert [cl.line for cl in m.clefs] == [2, 2, 2, 4, 4]
        assert [cl.octave_change for cl in m.clefs] == [2, None, None, None, -2]

        m.add_staff()
        assert len(m.clefs) == 6
        assert [cl.number for cl in m.clefs] == [1, 2, 3, 4, 5, 6]
        assert [cl.sign for cl in m.clefs] == ['G', 'G', 'G', 'F', 'F', 'F']
        assert [cl.line for cl in m.clefs] == [2, 2, 2, 4, 4, 4]
        assert [cl.octave_change for cl in m.clefs] == [2, None, None, None, None, -2]

    def test_measure_add_staff_and_change_clef_manually(self):
        m = Measure(1)
        m.add_staff()
        assert m.get_staff(1).clef.number is None
        bass_clef = BassClef()
        m.get_children()[0].clef = bass_clef
        assert m.get_staff(1).clef.number is None
        assert m.get_staff(1).clef == bass_clef

        m.add_staff()
        assert m.get_staff(1).clef.number == 1
        assert m.get_staff(2).clef.number == 2
        m.get_staff(2).clef = TrebleClef()
        assert m.get_staff(2).clef.number == 2

        assert m.get_staff(1).clef == bass_clef

        treble_clef = TrebleClef()
        m.add_child(Staff(number=3, clef=treble_clef))
        assert m.get_staff(3).clef.number == 3
        assert m.get_staff(3).clef == treble_clef

    def test_measure_false_show_keys(self):
        expected = """<measure number="1">
  <attributes>
    <divisions>1</divisions>
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
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</measure>
"""
        m = Measure(1)
        m.add_staff()
        m.key.show = False
        m._update_attributes()
        assert m.to_string() == expected

    def test_measure_false_show_time(self):
        expected = """<measure number="1">
  <attributes>
    <divisions>1</divisions>
    <key>
      <fifths>0</fifths>
    </key>
    <clef>
      <sign>G</sign>
      <line>2</line>
    </clef>
  </attributes>
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</measure>
"""
        m = Measure(1)
        m.add_staff()
        m.time.show = False
        m._update_attributes()
        assert m.to_string() == expected

    def test_measure_false_show_clef(self):
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
  </attributes>
  <note>
    <rest />
    <duration>4</duration>
    <voice>1</voice>
    <type>whole</type>
  </note>
</measure>
"""
        m = Measure(1)
        m.add_staff()
        m.clefs[0].show = False
        assert m.to_string() == expected


class TestMeasureBeatGrouping(TestCase):
    def test_measure_5_4(self):
        m = Measure(1, time=Time(5, 4))
        chords = m._add_chord(Chord(midis=60, quarter_duration=5))
        assert [ch.quarter_duration for ch in chords] == [3, 2]

    def test_measure_6_4(self):
        m = Measure(1, time=Time(6, 4))
        chords = m._add_chord(Chord(midis=60, quarter_duration=6))
        assert [ch.quarter_duration for ch in chords] == [6]

    def test_add_staff_to_score(self):
        score = Score()
        part = score.add_part('p1')
        measure = part.add_measure()
        st = measure.add_staff()
        assert st == measure.get_children()[-1]
