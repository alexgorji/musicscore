import copy
from unittest import skip, TestCase
from unittest.mock import Mock

from quicktions import Fraction

from musicscore import BassClef, Score, Part
from musicscore.accidental import Accidental
from musicscore.beat import Beat
from musicscore.chord import Chord, _split_copy, _group_chords, GraceChord, Rest
from musicscore.exceptions import ChordHasNoParentBeamError, DeepCopyException, ChordException, MusicTreeException, \
    ChordAddXPlacementException, RestCannotSetMidiError, \
    RestWithDisplayStepHasNoDisplayOctave, RestWithDisplayOctaveHasNoDisplayStep, GraceChordCannotHaveGraceNotesError, \
    AlreadyFinalizedError, ChordAlreadyHasNotesError, ChordHasNoNotesError, ChordTypeNotSetError, \
    ChordNumberOfDotsNotSetError, ChordTestError, ChordParentBeamError
from musicscore.midi import Midi
from musicscore.quarterduration import QuarterDuration
from musicscore.tests.util import ChordTestCase, create_test_objects, IdTestCase
from musicscore.tuplet import Tuplet
from musicscore.util import XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES, XML_DYNAMIC_CLASSES, XML_ORNAMENT_CLASSES, \
    XML_OTHER_NOTATIONS, XML_DIRECTION_TYPE_CLASSES
from musicxml.xmlelement.xmlelement import *


def get_chord_midi_values(chord):
    return [m.value for m in chord._midis]


class TestTreeChord(ChordTestCase):

    def test_mocks(self):
        assert self.mock_voice.number == 1
        assert self.mock_beat.up.number == 1
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        assert ch.up == self.mock_beat
        assert ch.up.up == self.mock_voice
        assert ch.up.up.up == self.mock_staff
        assert ch.up.up.up.up == self.mock_measure
        assert ch.get_parent_measure() == self.mock_measure

    def test_chord_init_midis(self):
        """
        Test all possible types of input midis
        """
        ch = Chord(70, 1)
        assert get_chord_midi_values(ch) == [70]
        ch = Chord([70, 50], 1)
        assert get_chord_midi_values(ch) == [50, 70]
        ch = Chord(0, 1)
        assert get_chord_midi_values(ch) == [0]
        ch = Chord(Midi(90, accidental=Accidental(mode='enharmonic')), 1)
        assert get_chord_midi_values(ch) == [90]
        ch = Chord([Midi(90, accidental=Accidental(mode='enharmonic')), 70], 1)
        assert get_chord_midi_values(ch) == [70, 90]

        with self.assertRaises(ValueError):
            Chord([0, 60], 1)

        """
        A grace note cannot be a rest.
        """
        with self.assertRaises(ValueError):
            Chord(0, 0)

    def test_chord_needs_parent_error(self):
        ch = Chord(70, 1)
        with self.assertRaises(ChordHasNoParentBeamError):
            ch.finalize()
        ch._parent = self.mock_beat
        ch.finalize()

    def test_init_quarter_durations(self):
        """
        Test values of quarter_duration
        """
        ch = Chord(90, 1.25)
        assert ch.quarter_duration == 1.25
        ch = Chord(80, 1.2)
        assert ch.quarter_duration == Fraction(1.2)
        assert ch.quarter_duration == 1.2
        assert ch.quarter_duration == Fraction(6 / 5)
        assert ch.quarter_duration == 6 / 5
        ch = Chord(80, 8)
        assert ch.quarter_duration == 8
        with self.assertRaises(TypeError):
            ch = Chord(80, '1.2')
        ch = Chord(70, Fraction(1, 4))
        assert ch.quarter_duration == 0.25
        ch = Chord(70, QuarterDuration(1, 4))
        assert ch.quarter_duration == 0.25

    def test_is_rest(self):
        """
        Test is_rest property
        """
        assert Chord(0, 1).is_rest
        assert not Chord(50, 1).is_rest

    def test_chord_attributes(self):
        """
        Test that a dot operator can set and get note attributes
        """
        c = Chord([60, 61, 62], 2)
        c._parent = self.mock_beat
        c.finalize()
        c.relative_x = 10
        assert c.relative_x == [10, 10, 10]
        c.relative_y = [None, 20, 10]
        assert c.relative_y == [None, 20, 10]
        c.relative_y = [10]
        assert c.relative_y == [10, 20, 10]
        c.default_y = [10]
        assert c.default_y == [10, None, None]

    def test_chord_one_note(self):
        c = Chord(70, 4, relative_x=10)
        c.midis[0].accidental.show = True
        c._parent = self.mock_beat
        c.type = 'whole'
        c.finalize()
        expected = """<note relative-x="10">
  <pitch>
    <step>B</step>
    <alter>-1</alter>
    <octave>4</octave>
  </pitch>
  <duration>4</duration>
  <voice>1</voice>
  <type>whole</type>
  <accidental>flat</accidental>
</note>
"""
        assert c.notes[0].to_string() == expected
        c.midis[0].value = 72
        c.type = 'whole'
        expected = """<note relative-x="10">
  <pitch>
    <step>C</step>
    <octave>5</octave>
  </pitch>
  <duration>4</duration>
  <voice>1</voice>
  <type>whole</type>
  <accidental>natural</accidental>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's midi (zero)
        c.midis[0].value = 0
        # c.finalize()

        expected = """<note relative-x="10">
  <rest />
  <duration>4</duration>
  <voice>1</voice>
  <type>whole</type>
</note>
"""
        assert c.notes[0].to_string() == expected
        c = Chord(midis=0, quarter_duration=2)
        # change chord's duration (not zero)
        c.quarter_duration = 1
        c._parent = self.mock_beat
        c.type = 'quarter'
        c.finalize()
        expected = """<note>
  <rest />
  <duration>1</duration>
  <voice>1</voice>
  <type>quarter</type>
</note>
"""
        assert c.notes[0].to_string() == expected
        c = Chord(0, 1)
        # change chord's duration (zero)
        with self.assertRaises(ValueError):
            c.quarter_duration = 0
        c.midis[0].value = 60
        # c.quarter_duration = 0
        # c._parent = self.mock_beat

    def test_chord_single_non_rest(self):
        """
        Test a chord with a non rest single midi
        """
        c = Chord(72, 2)
        c.midis[0].accidental.show = True
        c._parent = self.mock_beat
        c.finalize()

        c.xml_type = '16th'
        c.xml_stem = 'up'
        c.xml_staff = 1

        expected = """<note>
  <pitch>
    <step>C</step>
    <octave>5</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>16th</type>
  <accidental>natural</accidental>
  <stem>up</stem>
  <staff>1</staff>
</note>
"""
        assert c.notes[0].to_string() == expected
        c.midis[0].value = 61
        expected = """<pitch>
  <step>C</step>
  <alter>1</alter>
  <octave>4</octave>
</pitch>
"""
        assert c.notes[0].xml_pitch.to_string() == expected
        c.midis[0].value = 0
        # c.finalize()
        assert c.notes[0].xml_pitch is None
        assert c.notes[0].xml_rest is not None
        assert c.is_rest

    def test_chord_single_non_rest_midi_with_accidental(self):
        """
        Test chord with a non rest single midi with accidental set.
        """
        chord = Chord(Midi(70, accidental=Accidental(mode='sharp')), 1)
        chord._parent = self.mock_beat
        chord.finalize()
        expected = """<pitch>
    <step>A</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
"""
        assert chord.notes[0].xml_pitch.to_string() == expected

    def test_chord_as_rest(self):
        """
        Test chord with a rest midi
        """
        chord = Chord(0, 2)
        chord._parent = self.mock_beat
        chord.type = 'half'
        expected = """<note>
  <rest />
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""

        chord.finalize()
        assert chord.notes[0].to_string() == expected
        chord.midis = [60, 61]
        expected = """<pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
"""
        assert chord.notes[0].xml_pitch.to_string() == expected
        expected = """<pitch>
    <step>C</step>
    <alter>1</alter>
    <octave>4</octave>
  </pitch>
"""
        assert chord.notes[1].xml_pitch.to_string() == expected

    def test_chord_to_rest(self):
        chord = Chord(60, 2)
        chord._parent = self.mock_beat
        chord.type = chord.quarter_duration.get_type()
        chord.finalize()
        chord.to_rest()
        expected = """<note>
  <rest />
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""
        assert chord.notes[0].to_string() == expected
        assert len(chord.notes) == 1

    def test_chord_with_multiple_midis(self):
        """
        Test chord with a list of midis
        """

        chord = Chord([60, 62, 63], 2)
        chord.midis[1].accidental.show = True
        chord.midis[2].accidental.show = True
        chord._parent = self.mock_beat
        chord.type = chord.quarter_duration.get_type()
        chord.finalize()
        chord.xml_stem = 'up'
        expected_1 = """<note>
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
  <stem>up</stem>
</note>
"""
        expected_2 = """<note>
  <chord />
  <pitch>
    <step>D</step>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
  <accidental>natural</accidental>
  <stem>up</stem>
</note>
"""
        expected_3 = """<note>
  <chord />
  <pitch>
    <step>E</step>
    <alter>-1</alter>
    <octave>4</octave>
  </pitch>
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
  <accidental>flat</accidental>
  <stem>up</stem>
</note>
"""
        for note, expected in zip(chord.notes, [expected_1, expected_2, expected_3]):
            assert note.to_string() == expected

    def test_group_chords(self):
        chords = [Chord(60, qd) for qd in [1 / 6, 1 / 6, 1 / 6, 1 / 10, 3 / 10, 1 / 10]]
        with self.assertRaises(ValueError):
            assert _group_chords(chords, [1 / 2, 1 / 2, 1 / 2])
        assert _group_chords(chords, [1 / 2, 1 / 2]) == [chords[:3], chords[3:]]
        assert _group_chords(chords, [1 / 3, 2 / 3]) == [chords[:2], chords[2:]]
        assert _group_chords(chords, [1 / 4, 3 / 4]) is None

    def test_has_same_pitches(self):
        ch1 = Chord([60, Midi(61), 62], 1)
        ch2 = Chord([60, Midi(61)], 1)
        assert not ch1.has_same_pitches(ch2)
        ch2 = Chord([60, Midi(61), 62], 1)
        assert ch1.has_same_pitches(ch2)
        ch2 = Chord([60, Midi(61, accidental=Accidental(mode='flat')), 62], 1)
        assert not ch1.has_same_pitches(ch2)

    def test_add_lyric(self):
        ch = Chord(60, 2)
        ch._parent = self.mock_beat
        ch.add_lyric('test')
        ch.finalize()
        assert ch.notes[0].xml_lyric is not None
        assert ch.notes[0].xml_lyric.xml_text.value_ == 'test'

    def test_get_staff_number(self):
        ch = Chord(60, 2)
        ch._parent = self.mock_beat
        assert ch.get_staff_number() is None
        self.mock_staff.number = 1
        assert ch.get_staff_number() == 1

    def test_add_clef(self):
        ch = Chord(60, 2)
        assert ch.clef is None
        cl = BassClef()
        ch.clef = cl
        assert ch.clef == cl
        with self.assertRaises(TypeError):
            ch.clef = 'bla'

    def test_break_beam(self):
        ch = Chord(60, 2)
        self.assertFalse(ch.broken_beam)
        ch.broken_beam = True
        self.assertTrue(ch.broken_beam)
        ch = Chord(60, 2)
        self.assertFalse(ch.broken_beam)
        ch.break_beam()
        self.assertTrue(ch.broken_beam)

    @skip
    def test_percussion_notation(self):
        self.fail('Incomplete')

    @skip
    def test_finger_tremolo(self):
        self.fail('Incomplete')

    def test_deepcopy_chord(self):
        chord = Chord([60, 62], 2)
        chord.add_tie('start')
        copied = copy.deepcopy(chord)
        assert [midi.value for midi in copied.midis] == [midi.value for midi in chord.midis]
        assert [id(midi) for midi in copied.midis] != [id(midi) for midi in chord.midis]
        assert chord.quarter_duration.value == copied.quarter_duration.value
        assert id(chord.quarter_duration) != id(copied.quarter_duration)
        chord._parent = self.mock_beat
        chord.finalize()
        with self.assertRaises(DeepCopyException):
            copy.deepcopy(chord)
        # chord.add_dynamics('p')
        # chord.add_lyric('something')
        # chord.add_x(XMLAccent())
        # chord.add_x(XMLUpBow())
        # chord.add_x(XMLAccidentalMark())
        # chord.add_x(XMLFf())

    def test_add_midi(self):
        chord = Chord([60, 62], 2)
        m = Midi(63)
        chord.add_midi(m)
        assert [midi.value for midi in chord.midis] == [60, 62, 63]
        assert chord.midis[-1] == m
        chord.add_midi(58)
        assert [midi.value for midi in chord.midis] == [58, 60, 62, 63]
        chord.add_midi(60)
        assert [midi.value for midi in chord.midis] == [58, 60, 60, 62, 63]

        chord._parent = self.mock_beat
        chord.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            chord.add_midi(80)

    def test_add_direction_type(self):
        score = Score()
        p = score.add_part('part-1')
        for dt_class in XML_DIRECTION_TYPE_CLASSES:
            chord = Chord(midis=60, quarter_duration=4)
            if dt_class == XMLSymbol:
                dt_obj = dt_class('0')
            else:
                dt_obj = dt_class()
            if dt_class == XMLDynamics:
                assert self.assertRaises(ChordException)
            else:
                chord.add_direction_type(dt_obj, 'above')
                assert dt_obj in chord.xml_direction_types['above']
                assert chord.xml_direction_types['above'] == [dt_obj]
                p.add_chord(chord)
        p.finalize()

    def test_add_direction_type_wrong_type(self):
        chord = Chord(60, 4)
        with self.assertRaises(TypeError):
            chord.add_direction_type(XMLFermata())

    def test_chord_to_string(self):
        p = Part('p1')
        ch = Chord(60, 1)
        p.add_chord(ch)
        ch.finalize()
        with self.assertRaises(MusicTreeException):
            ch.to_string()

    def test_get_x(self):
        def test_get_objects(*classes):
            chord = Chord(60, 1)
            cl1, cl2, cl3 = classes
            dt1 = chord.add_x(cl1())
            dt2 = chord.add_x(cl1())
            dt3 = chord.add_x(cl2())
            assert chord.get_x(cl1) == [dt1, dt2]
            assert chord.get_x(cl2) == [dt3]
            assert chord.get_x(cl3) == []

        # oranment
        test_get_objects(XML_ORNAMENT_CLASSES[0], XML_ORNAMENT_CLASSES[1], XML_ORNAMENT_CLASSES[2])
        # articualtion
        test_get_objects(XML_ARTICULATION_CLASSES[0], XML_ARTICULATION_CLASSES[1], XML_ARTICULATION_CLASSES[2])
        # technical
        test_get_objects(XML_TECHNICAL_CLASSES[0], XML_TECHNICAL_CLASSES[1], XML_TECHNICAL_CLASSES[2])
        # other notations
        test_get_objects(XML_OTHER_NOTATIONS[0], XML_OTHER_NOTATIONS[1], XML_OTHER_NOTATIONS[2])
        # direction type
        test_get_objects(XML_DIRECTION_TYPE_CLASSES[0], XML_DIRECTION_TYPE_CLASSES[1], XML_DIRECTION_TYPE_CLASSES[2])

        # ornament or notation
        chord = Chord(60, 1)
        cl1 = XMLAccidentalMark
        dt1 = chord.add_x(cl1('sharp'), parent_type='ornament')
        dt2 = chord.add_x(cl1('flat'), parent_type='ornament')
        dt3 = chord.add_x(cl1('flat'), parent_type='notation')
        assert chord.get_x(cl1) == [dt1, dt2, dt3]

    def test_get_wedges(self):
        chord = Chord(60, 1)
        dt1 = chord.add_x(XMLWedge(type='crescendo'))
        dt2 = chord.add_x(XMLWedge(type='continue'))
        dt3 = chord.add_x(XMLWedge(type='stop'))
        assert chord.get_wedges() == [dt1, dt2, dt3]

    def test_get_slurs(self):
        chord = Chord(60, 1)
        dt1 = chord.add_x(XMLSlur(type='start'))
        dt2 = chord.add_x(XMLSlur(type='continue'))
        dt3 = chord.add_x(XMLSlur(type='stop'))
        assert chord.get_slurs() == [dt1, dt2, dt3]

    def test_get_words(self):
        chord = Chord(60, 1)
        dt1 = chord.add_x(XMLWords('something'))
        dt2 = chord.add_x(XMLWords('something else'))
        assert chord.get_words() == [dt1, dt2]

    def test_get_brackets(self):
        chords = [Chord(60, 1) for _ in range(3)]
        b1, b2, b3 = chords[0].add_x(XMLBracket()), chords[1].add_x(XMLBracket()), chords[2].add_x(XMLBracket())
        assert [ch.get_brackets()[0] for ch in chords] == [b1, b2, b3]

    def test_add_arpeggio_normal(self):
        ch = Chord([60, 64, 67], 1)
        assert not ch.arpeggio
        ch._parent = self.mock_beat
        ch.arpeggio = 'normal'
        assert ch.arpeggio == 'normal'
        ch.finalize()
        for n in ch.notes:
            assert n.xml_notations.xml_arpeggiate
            assert n.xml_notations.xml_arpeggiate.direction is None

    def test_add_arpeggio_up(self):
        ch = Chord([60, 64, 67], 1)
        assert not ch.arpeggio
        ch._parent = self.mock_beat
        ch.arpeggio = 'up'
        assert ch.arpeggio == 'up'
        ch.finalize()
        for n in ch.notes:
            assert n.xml_notations.xml_arpeggiate
            if n == ch.notes[0]:
                assert n.xml_notations.xml_arpeggiate.direction == 'up'

    def test_add_arpeggio_bottom(self):
        ch = Chord([60, 64, 67], 1)
        assert not ch.arpeggio
        ch._parent = self.mock_beat
        ch.arpeggio = 'down'
        assert ch.arpeggio == 'down'
        ch.finalize()
        for n in ch.notes:
            assert n.xml_notations.xml_arpeggiate
            if n == ch.notes[0]:
                assert n.xml_notations.xml_arpeggiate.direction == 'down'

    def test_add_none_arpeggio(self):
        ch = Chord([60, 64, 67], 1)
        assert not ch.arpeggio
        ch._parent = self.mock_beat
        ch.arpeggio = 'none'
        assert ch.arpeggio == 'none'
        ch.finalize()
        for n in ch.notes:
            if n == ch.notes[0]:
                assert n.xml_notations.xml_non_arpeggiate
                assert n.xml_notations.xml_non_arpeggiate.type == 'bottom'
            elif n == ch.notes[-1]:
                assert n.xml_notations.xml_non_arpeggiate
                assert n.xml_notations.xml_non_arpeggiate.type == 'top'


class TestTreeRest(ChordTestCase):
    def test_rest_init(self):
        r = Rest(4)
        r._parent = self.mock_beat
        assert isinstance(r, Rest)
        assert isinstance(r, Chord)
        assert r.midis[0].value == 0
        r.finalize()
        n = r.notes[0]
        assert r.display_step == r.display_octave == n.xml_object.xml_rest.xml_display_step == n.xml_object.xml_rest.xml_display_octave is None
        assert r.quarter_duration == 4
        r = Rest(4, display_step='C', display_octave=4)
        r._parent = self.mock_beat
        r.finalize()
        n = r.notes[0]
        assert r.display_step == n.xml_object.xml_rest.xml_display_step.value_ == 'C'
        assert r.display_octave == n.xml_object.xml_rest.xml_display_octave.value_ == 4
        r = Rest(4, measure='yes')
        assert r.measure == 'yes'
        r._parent = self.mock_beat
        r.finalize()
        n = r.notes[0]
        assert n.xml_object.xml_rest.measure == 'yes'
        with self.assertRaises(RestCannotSetMidiError):
            Rest(midis=0, quarter_duration=2)
        with self.assertRaises(TypeError):
            Rest()
        with self.assertRaises(RestWithDisplayStepHasNoDisplayOctave):
            r = Rest(4, display_step='D')
            r._parent = self.mock_beat
            r.finalize()
        with self.assertRaises(RestWithDisplayOctaveHasNoDisplayStep):
            r = Rest(4, display_octave=4)
            r._parent = self.mock_beat
            r.finalize()
        with self.assertRaises(TypeError):
            Rest(4, display_step='H', display_octave=2)
        with self.assertRaises(TypeError):
            Rest(4, display_step='C', display_octave=2.2)
        with self.assertRaises(TypeError):
            Rest(4, display_step='C', display_octave=-2)


class TestTies(ChordTestCase):

    def test_add_tie_ties_midis(self):
        ch = Chord([60, 63], 1)
        ch._parent = self.mock_beat
        ch.add_tie('start')
        for midi in ch.midis:
            assert midi._ties == {'start'}
        ch.finalize()
        assert [n.is_tied for n in ch.notes] == [True, True]

    def test_tied_midis(self):
        m1 = Midi(60)
        m1.add_tie('start')
        m2 = Midi(61)
        m2.add_tie('start')
        ch = Chord([m1, m2], 1)
        ch._parent = self.mock_beat
        ch.finalize()
        assert [n.is_tied for n in ch.notes] == [True, True]

    def test_split_tied_copy(self):
        ch = Chord(midis=60, quarter_duration=1)
        copied = _split_copy(ch)
        assert ch.midis[0]._ties == copied.midis[0]._ties == set()

    def test_tie_one_note(self):
        ch1 = Chord([60, 63], 1)
        ch2 = Chord([60, 65], 1)
        ch1.midis[0].add_tie('start')
        ch2.midis[0].add_tie('stop')
        ch1._parent = self.mock_beat
        ch2._parent = self.mock_beat
        ch1.finalize()
        ch2.finalize()
        assert [n.is_tied for n in ch1.notes] == [True, False]
        assert [n.is_tied_to_previous for n in ch2.notes] == [True, False]

    def test_untie_one_note(self):
        ch = Chord([60, 61], 1)
        ch.add_tie('start')
        ch._parent = self.mock_beat
        ch.finalize()
        assert [n.is_tied for n in ch.notes] == [True, True]
        # print(ch.notes)
        ch.midis[0].remove_tie('start')
        assert [n.is_tied for n in ch.notes] == [False, True]

    def test_chord_tie_untie(self):
        ch1 = Chord([60, 61], 1)
        ch2 = Chord([60, 61], 1)
        ch1.add_tie('start')
        ch2.add_tie('stop')
        ch1._parent = self.mock_beat
        ch2._parent = self.mock_beat
        ch1.finalize()
        ch2.finalize()
        assert [n.is_tied for n in ch1.notes] == [True, True]
        assert [n.is_tied for n in ch2.notes] == [False, False]
        assert [n.is_tied_to_previous for n in ch2.notes] == [True, True]

    def test_chord_change_tie_after_finalizing(self):
        ch1 = Chord([60, 61], 1)
        ch2 = Chord([60, 61], 1)
        ch1._parent = self.mock_beat
        ch2._parent = self.mock_beat
        ch1.finalize()
        ch2.finalize()

        ch1.add_tie('start')
        ch2.midis[1].add_tie('stop')

        assert [n.is_tied for n in ch1.notes] == [True, True]
        assert [n.is_tied for n in ch2.notes] == [False, False]
        assert [n.is_tied_to_previous for n in ch2.notes] == [False, True]

    def test_chord_all_midis_tied_to_next_or_previous(self):
        ch = Chord([60, 61, 62], 1)
        for m in ch.midis:
            m.add_tie('start')
        assert ch.all_midis_are_tied_to_next
        ch.midis[1].remove_tie('start')
        assert not ch.all_midis_are_tied_to_next
        ch.midis[0].add_tie('stop')
        assert not ch.all_midis_are_tied_to_previous
        for m in ch.midis:
            m.add_tie('stop')
        assert ch.all_midis_are_tied_to_previous


class TestSplit(TestCase):

    def test_set_original_starting_ties(self):
        ch = Chord(midis=[60, 61], quarter_duration=1)
        ch._set_original_starting_ties(ch)
        copied = _split_copy(ch)
        assert copied._original_starting_ties == [set(), set()]
        ch.midis[0].add_tie('start')
        ch._set_original_starting_ties(ch)
        assert copied._original_starting_ties == [set(), set()]

    def test_split_copy(self):
        ch = Chord(midis=[Midi(61, accidental=Accidental(mode='sharp'))], quarter_duration=2, offset=0.5)
        copied = _split_copy(ch)
        assert ch.midis != copied.midis
        assert ch.midis[0].value == copied.midis[0].value
        assert ch.midis[0].accidental != copied.midis[0].accidental
        assert ch.midis[0].accidental.mode == copied.midis[0].accidental.mode
        copied.midis[0].accidental.show = False
        assert ch.midis[0].accidental.show is None
        assert copied.midis[0].accidental.show is False

    def test_tied_split_copy(self):
        ch = Chord(midis=61, quarter_duration=2)
        ch.add_tie('start')
        copied = _split_copy(ch)
        for m in copied.midis:
            assert m._ties == set()

    def test_split_quarter_durations(self):
        ch = Chord(midis=60, quarter_duration=4)
        copied = _split_copy(ch)
        assert id(ch.quarter_duration) != id(copied.quarter_duration)
        ch.quarter_duration = 2
        assert copied.quarter_duration == 4
        assert ch.quarter_duration == 2

        ch = Chord(midis=60, quarter_duration=5)
        beats = [Beat(1), Beat(1), Beat(1), Beat(1)]
        quarter_durations = ch.quarter_duration._get_beatwise_sections(beats=beats)
        ch.quarter_duration = quarter_durations[0][0]
        copied = _split_copy(ch, quarter_durations[1])
        assert [ch.quarter_duration, copied.quarter_duration] == [4, 1]


class TestAddGraceChord(ChordTestCase):
    def test_add_grace_chord_parameters(self):
        ch = Chord(60, 1)
        g1 = gch = ch.add_grace_chord(midis_or_grace_chord=60)
        assert gch.midis[0].value == 60
        in_gch = GraceChord(61)
        g2 = gch = ch.add_grace_chord(midis_or_grace_chord=in_gch)
        assert gch == in_gch
        g3 = gch = ch.add_grace_chord(midis_or_grace_chord=[62, 63])
        assert [m.value for m in gch.midis] == [62, 63]
        g4 = gch = ch.add_grace_chord(64)
        assert gch.midis[0].value == 64
        g5 = gch = ch.add_grace_chord(midis_or_grace_chord=65, type='16th')
        assert gch.midis[0].value == 65
        assert gch.type == '16th'
        in_gch = GraceChord(61, type='16th')
        g6 = gch = ch.add_grace_chord(midis_or_grace_chord=in_gch)
        assert gch == in_gch
        assert gch.type == '16th'
        with self.assertRaises(ValueError):
            ch.add_grace_chord(midis_or_grace_chord=GraceChord(66, type='quarter'), type='16th')
        g7 = gch = ch.add_grace_chord(67, type='16th')
        assert gch.midis[0].value == 67
        assert gch.type == '16th'
        g8 = gch = ch.add_grace_chord(68, type='16th', position='after')
        assert gch.position == 'after'
        assert gch.midis[0].value == 68
        assert gch.type == '16th'
        with self.assertRaises(ValueError):
            ch.add_grace_chord(GraceChord(66, type='quarter'), position='after')
        assert ch.get_grace_chords(position='before') == [g1, g2, g3, g4, g5, g6, g7]
        assert ch.get_grace_chords(position='after') == [g8]

    def test_add_grace_chord_before_and_after_argument(self):
        ch = Chord(60, 1)
        midis_or_chord = [62, [63, 65], GraceChord(66)]
        before_chords = [ch.add_grace_chord(x) for x in midis_or_chord]
        assert ch._grace_chords['before'] == before_chords

        midis_or_chord = [67, [68, 70], GraceChord(71, position='after')]
        after_chords = [
            ch.add_grace_chord(x, position='after') if not isinstance(x, GraceChord) else ch.add_grace_chord(x) for x in
            midis_or_chord]
        assert ch._grace_chords['after'] == after_chords

    def test_add_grace_chord_generates_grace_chords(self):
        ch = Chord(60, 1)
        with self.assertRaises(TypeError):
            ch.add_grace_chord()
        gc1 = ch.add_grace_chord(60)
        gc2 = ch.add_grace_chord(61, type='quarter')
        gc3 = ch.add_grace_chord(GraceChord(midis=[62, 64]))
        gc4 = ch.add_grace_chord(GraceChord(63, type='16th'))
        all_gcs = [gc1, gc2, gc3, gc4]
        assert [[m.value for m in gc.midis] for gc in all_gcs] == [[60], [61], [62, 64], [63]]
        assert [gc.type for gc in all_gcs] == [None, 'quarter', None, '16th']

    def test_add_grace_chord_finalize(self):
        part = Part('p1')
        ch = Chord(midis=[60, 63], quarter_duration=4)
        midis_or_chord = [62, [63, 65], GraceChord(66)]
        before_chords = [ch.add_grace_chord(x) for x in midis_or_chord]
        midis_or_chord = [67, [68, 70], GraceChord(71, position='after')]
        after_chords = [
            ch.add_grace_chord(x, position='after') if not isinstance(x, GraceChord) else ch.add_grace_chord(x) for x in
            midis_or_chord]
        part.add_chord(ch)
        with self.assertRaises(ChordException):
            ch.add_grace_chord(80)
        part.finalize()
        assert len(part.get_chords()) == 7

    def test_grace_chords_are_added_to_right_voice(self):
        part = Part('p1')
        ch = Chord(midis=[60, 63], quarter_duration=4)
        gch1 = ch.add_grace_chord(80)
        gch2 = ch.add_grace_chord(90, position='after')
        part.add_chord(ch, staff_number=2, voice_number=2)
        part.finalize()
        assert part.get_voice(1, 2, 2).get_chords() == [gch1, ch, gch2]
        for c in [gch1, ch, gch2]:
            assert c.voice_number == 2
            assert c.get_staff_number() == 2

    def test_grace_chords_after_the_last_chord_in_measure(self):
        part = Part('p1')
        ch = Chord(60, 4)
        gch = ch.add_grace_chord(80, position='after')
        part.add_chord(ch)
        part.add_chord(Chord(90, 1))
        part.finalize()
        assert gch in part.get_measure(1).get_chords()

    def test_error_grace_chord_add_grace_chord(self):
        gch = GraceChord(60)
        with self.assertRaises(GraceChordCannotHaveGraceNotesError):
            gch.add_grace_chord(80)

    def test_grace_chords_after_to_right_beat(self):
        part = Part('p1')
        ch = Chord(60, 1)
        gch = ch.add_grace_chord(80, position='after')
        part.add_chord(ch)
        part.add_chord(Chord(90, 3))
        assert gch in part.get_beat(1, 1, 1, 1).get_children()


class TestAddX(ChordTestCase):
    # def setUp(self):
    #     super().setUp()
    #     self.score = Score()
    #     self.part = self.score.add_part('p1')

    def test_add_x_parent_type(self):
        ch = Chord(60, 1)
        ch.add_x(XML_DIRECTION_TYPE_CLASSES[0]())

    def test_add_x_placement(self):
        def add_type_and_placement(type, xml_object=None):
            above_part = Part(f"above-{type}-{xml_object.name}") if xml_object else Part(f"above-{type}")
            below_part = Part(f"below-{type}-{xml_object.name}") if xml_object else Part(f"below-{type}")
            if not xml_object:
                above_objects = create_test_objects(type)
                below_objects = create_test_objects(type)
            else:
                above_objects = [xml_object]
                below_objects = [xml_object.__deepcopy__()]

            for obj in above_objects:
                ch = Chord(60, 1)
                try:
                    ch.add_x(obj, placement='above', parent_type=type)
                except ChordAddXPlacementException:
                    ch.add_x(obj, placement=None, parent_type=type)
                above_part.add_chord(ch)
            for obj in below_objects:
                ch = Chord(60, 1)
                try:
                    ch.add_x(obj, placement='below', parent_type=type)
                except ChordAddXPlacementException:
                    ch.add_x(obj, placement=None, parent_type=type)
                below_part.add_chord(ch)

            above_part.finalize()
            below_part.finalize()
            if type == 'direction_type':
                for p in ['above', 'below']:
                    directions = [d for m in eval(f"{p}_part.get_children()") for d in
                                  [c for c in m.xml_object.get_children() if isinstance(c, XMLDirection)]]
                    assert len(directions) == len(above_objects)
                    for x in directions:
                        assert x.placement == p

            elif type in ['technical', 'ornament', 'articulation']:
                for p in ['above', 'below']:
                    notations = [notation for measure in eval(f'{p}_part').get_children() for note in
                                 [x for x in measure.xml_object.get_children() if isinstance(x, XMLNote)] for notation
                                 in
                                 [y for y in note.get_children() if isinstance(y, XMLNotations)]]
                    assert len(notations) == len(above_objects)
                    for x in notations:
                        if x.get_children()[0].get_children()[0].__class__ not in [XMLFret, XMLBend]:
                            assert x.get_children()[0].get_children()[0].placement == p
            else:
                raise NotImplementedError(f'testing type {type}')

        # direction_type objects
        add_type_and_placement('direction_type')

        # technical objects
        add_type_and_placement('technical')

        # ornament objects
        add_type_and_placement('ornament')

        # articulation objects
        add_type_and_placement('articulation')

        # notation only objects does not accept placement (except fermata)
        notation_object = XMLArpeggiate()
        ch = Chord(60, 1)
        with self.assertRaises(ChordAddXPlacementException):
            ch.add_x(notation_object, placement='above', parent_type='notation')
        ch.add_x(notation_object, placement=None, parent_type='notation')

        # mixed below and above
        part = Part('mixed_placements')
        x_objects = [XMLTenuto(), XMLStaccato(), XMLAccent()]
        placements = ['below', 'below', 'above']
        ch = Chord(60, 1)
        for obj, plc in zip(x_objects, placements):
            ch.add_x(obj, placement=plc)
        part.add_chord(ch)
        part.finalize()
        notations = [notation for measure in part.get_children() for note in
                     [x for x in measure.xml_object.get_children() if isinstance(x, XMLNote)] for notation in
                     [y for y in note.get_children() if isinstance(y, XMLNotations)]]
        for index, x in enumerate(notations[0].xml_articulations.get_children()):
            assert x.placement == placements[index]

        # fermata placement is translated in fermata types inverted or upright
        fermatas = [XMLFermata(), XMLFermata()]
        placements = ['above', 'below']
        ch = Chord(60, 1)
        for f, p in zip(fermatas, placements):
            ch.add_x(f, placement=p)

        for f, t in zip(fermatas, ['upright', 'inverted']):
            assert f.type == t

    def test_add_articulation_after_creating_notes(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        staccato = ch.add_x(XMLStaccato())
        ch.finalize()
        assert ch.notes[0].xml_notations.xml_articulations.get_children() == [staccato]
        assert isinstance(ch.notes[0].xml_notations.xml_articulations.get_children()[0], XMLStaccato)
        accent = ch.add_x(XMLAccent())
        assert ch.notes[0].xml_notations.xml_articulations.get_children() == [staccato, accent]

    def test_add_multiple_articulations(self):
        articulation_classes = XML_ARTICULATION_CLASSES[:3]
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        for a in articulation_classes:
            ch.add_x(a())
        assert len(ch._xml_articulations) == 3
        ch.finalize()
        n = ch.notes[0]
        assert n.xml_notations.xml_articulations is not None
        assert [type(a) for a in n.xml_notations.xml_articulations.get_children()] == articulation_classes

    def test_chord_add_x_as_object_articulation(self):
        for obj in create_test_objects('articulation'):
            ch = Chord(60, 1)
            ch.add_x(obj)
            ch._parent = self.mock_beat
            ch.finalize()
            assert ch.notes[0].xml_notations.xml_articulations.get_children()[0] == obj

    def test_chord_add_x_as_object_technical(self):
        for obj in create_test_objects('technical'):
            ch = Chord(60, 1)
            ch.add_x(obj)
            ch._parent = self.mock_beat
            ch.finalize()
            assert ch.notes[0].xml_notations.xml_technical.get_children()[0] == obj

    def test_chord_add_x_as_object_dynamics(self):
        for cls in XML_DYNAMIC_CLASSES:
            ch = Chord(60, 1)
            ch.add_x(cls(), parent_type='notation')
            ch._parent = self.mock_beat
            ch.finalize()
            assert isinstance(ch.notes[0].xml_notations.xml_dynamics.get_children()[0], cls)

    def test_chord_add_x_as_object_ornaments(self):
        for obj in create_test_objects('ornament'):
            ch = Chord(60, 1)
            if isinstance(obj, XMLAccidentalMark):
                ch.add_x(obj, parent_type='ornament')
            else:
                ch.add_x(obj)
            ch._parent = self.mock_beat
            ch.finalize()
            assert ch.notes[0].xml_notations.xml_ornaments.get_children()[0] == obj

    def test_chord_add_x_trill_with_wavy_line_and_accidental_mark(self):
        ch = Chord(60, 1)
        ch.add_x(XMLTrillMark())
        ch.add_x(XMLAccidentalMark('sharp'), parent_type='ornament')
        ch.add_x(XMLWavyLine(type='start', relative_x=0))
        ch.add_x(XMLWavyLine(type='stop', relative_x=20))
        ch._parent = self.mock_beat
        ch.finalize()
        expected = """<ornaments>
      <trill-mark />
      <accidental-mark>sharp</accidental-mark>
      <wavy-line type="start" relative-x="0" />
      <wavy-line type="stop" relative-x="20" />
    </ornaments>
"""
        assert ch.notes[0].xml_notations.xml_ornaments.to_string() == expected

    def test_chord_add_x_as_object_other_notations(self):
        for cls in XML_OTHER_NOTATIONS:
            ch = Chord(60, 1)
            ch.add_x(cls())
            ch._parent = self.mock_beat
            ch.finalize()
            assert isinstance(ch.notes[0].xml_notations.get_children()[0], cls)

    def test_add_xml_wedge_objects(self):
        wedges = [XMLWedge(type=val) for val in ['crescendo', 'stop', 'diminuendo', 'stop']]
        for wedge in wedges:
            ch = Chord(60, 4)
            ch._parent = self.mock_beat
            ch.add_wedge(wedge)
            ch.finalize()
            assert len(ch._xml_directions) == 1
            d = ch._xml_directions[0]
            assert d.placement == 'below'
            assert d.xml_direction_type.xml_wedge == wedge

    def test_add_wedge_string(self):
        wedges = ['crescendo', 'stop', 'diminuendo', 'stop']
        for wedge in wedges:
            ch = Chord(60, 4)
            ch._parent = self.mock_beat
            ch.add_wedge(wedge)
            ch.finalize()
            assert len(ch._xml_directions) == 1
            d = ch._xml_directions[0]
            assert d.placement == 'below'
            assert d.xml_direction_type.xml_wedge.type == wedge

    def test_add_words(self):
        ch = Chord(60, 4)
        ch._parent = self.mock_beat
        texts = ['Below', 'Above', 'FontSize', 'Bold']
        xml_words_objects = [ch.add_words(texts[0], placement='below'),
                             ch.add_words(texts[1]),
                             ch.add_words(texts[2], font_size=18, relative_y=30),
                             ch.add_words(texts[3], font_weight='bold', relative_y=60)]
        ch.finalize()
        assert set(xml_words_objects) == set([d.xml_direction_type.xml_words for d in ch._xml_directions])

        for obj, t in zip(xml_words_objects, texts):
            assert obj.value_ == t

        for obj, p in zip(xml_words_objects, ['below', 'above', 'above', 'above']):
            assert obj.up.up.placement == p
        for fs, obj in zip([None, None, 18, None], xml_words_objects):
            assert obj.font_size == fs
        for fw, obj in zip([None, None, None, 'bold'], xml_words_objects):
            assert obj.font_weight == fw
        for ry, obj in zip([None, None, 30, 60], xml_words_objects):
            assert obj.relative_y == ry

        ch = Chord(60, 4)
        ch._parent = self.mock_beat

        xml_words = ch.add_words(XMLWords('something', font_size=10, relative_y=20), placement='below', font_size=20)
        ch.finalize()
        d = ch._xml_directions[0]
        assert d.xml_direction_type.xml_words.value_ == 'something'
        assert d.placement == 'below'
        assert xml_words.font_size == 20
        assert xml_words.relative_y == 20


class TestAddAfterNotes(IdTestCase):
    def test_add_after_notes(self):
        part = Part('p1')
        chords = [Chord([60, 62], 2), Chord(64, 2)]
        chords[0].add_dynamics('ff')
        [part.add_chord(ch) for ch in chords]
        b = XMLBarline(location='middle')
        b.xml_bar_style = 'dashed'
        chords[0].add_xml_element_after_notes(b)
        part.finalize()
        m = part.get_measure(1)
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
    <direction placement="below">
      <direction-type>
        <dynamics>
          <ff />
        </dynamics>
      </direction-type>
    </direction>
    <note>
      <pitch>
        <step>C</step>
        <octave>4</octave>
      </pitch>
      <duration>2</duration>
      <voice>1</voice>
      <type>half</type>
    </note>
    <note>
      <chord />
      <pitch>
        <step>D</step>
        <octave>4</octave>
      </pitch>
      <duration>2</duration>
      <voice>1</voice>
      <type>half</type>
    </note>
    <barline location="middle">
      <bar-style>dashed</bar-style>
    </barline>
    <note>
      <pitch>
        <step>E</step>
        <octave>4</octave>
      </pitch>
      <duration>2</duration>
      <voice>1</voice>
      <type>half</type>
    </note>
  </measure>
"""
        assert m.to_string() == expected


class TestTypeAndNumberOfDots(IdTestCase):
    def test_chord_type_error(self):
        ch = Chord(60, 1)
        with self.assertRaises(ValueError):
            ch.type = 'bla'

    def test_chord_number_of_dots_error(self):
        ch = Chord(60, 1)
        with self.assertRaises(TypeError):
            ch.number_of_dots = None
        with self.assertRaises(TypeError):
            ch.number_of_dots = '1'
        with self.assertRaises(ValueError):
            ch.number_of_dots = -1

    def test_chord_type_attribute_with_update(self):
        p = Part('p0')
        ch = Chord([60, 61], 2)
        p.add_chord(ch)
        p.finalize()
        assert ch.get_children()[0].xml_type.value_ == 'half'
        assert ch.get_children()[1].xml_type.value_ == 'half'
        p = Part('p1')
        ch = Chord([60, 61], 2)
        ch.type = 'whole'
        p.add_chord(ch)
        p.finalize()
        assert ch.get_children()[0].xml_type.value_ == 'whole'
        assert ch.get_children()[1].xml_type.value_ == 'whole'
        with self.assertRaises(ChordAlreadyHasNotesError):
            ch.type = 'half'
        gch = Chord([60, 61], 0)
        assert gch.type is None
        p = Part('p2')
        p.add_chord(gch)
        # print(p.get_beats()[0])
        # print(p.get_beats()[0].is_filled)
        p.finalize()

        assert gch.get_children()[0].xml_type is None
        assert gch.get_children()[1].xml_type is None

        p = Part('p3')
        p.add_chord(Chord(60, 1))
        gch = GraceChord([60, 61])
        assert gch.type is None
        p.add_chord(gch)
        p.finalize()

        assert gch.get_children()[0].xml_type is None
        assert gch.get_children()[1].xml_type is None

        p = Part('p4')
        gch = GraceChord([60, 61])
        gch.type = 'half'
        assert gch.type == 'half'
        p.add_chord(gch)
        p.finalize()
        assert gch.get_children()[0].xml_type.value_ == 'half'
        assert gch.get_children()[1].xml_type.value_ == 'half'

    def test_chord_number_of_dots_with_update(self):
        p = Part('p1')
        [p.add_chord(Chord([60, 61], qd)) for qd in [1, 0.75, 0.25]]
        assert {ch.number_of_dots for ch in p.get_chords()} == {None}
        p.finalize()
        assert [ch.number_of_dots for ch in p.get_chords()[:3]] == [0, 1, 0]
        ch = p.get_chords()[1]
        assert len(ch.get_children()[0].xml_object.get_children_of_type(XMLDot)) == 1
        assert len(ch.get_children()[1].xml_object.get_children_of_type(XMLDot)) == 1
        with self.assertRaises(ChordAlreadyHasNotesError):
            ch.number_of_dots = 3

        p = Part('p2')
        gch = GraceChord([60, 61])
        gch.number_of_dots = 3
        p.add_chord(gch)
        p.finalize()
        assert len(gch.get_children()[0].xml_object.get_children_of_type(XMLDot)) == 3
        assert len(gch.get_children()[1].xml_object.get_children_of_type(XMLDot)) == 3

    def test_number_of_beams(self):
        chord = Chord(60, 1)
        with self.assertRaises(ChordTypeNotSetError):
            chord.number_of_beams
        chord.type = 'quarter'
        assert chord.number_of_beams == 0
        chord.type = '32nd'
        assert chord.number_of_beams == 3

    def test_test_quarter_duration(self):
        chord = Chord(60, 1 / 3)
        with self.assertRaises(ChordHasNoParentBeamError):
            chord.check_printed_duration()
        chord._parent = Mock()
        chord._parent.quarter_duration = None
        with self.assertRaises(ChordParentBeamError):
            chord.check_printed_duration()
        chord._parent.quarter_duration = 1
        chord._parent.get_subdivision.return_value = None
        with self.assertRaises(ChordParentBeamError):
            chord.check_printed_duration()
        chord._parent.get_subdivision.return_value = 3
        with self.assertRaises(ChordTypeNotSetError):
            chord.check_printed_duration()
        chord.type = 'eighth'
        with self.assertRaises(ChordNumberOfDotsNotSetError):
            chord.check_printed_duration()
        chord.number_of_dots = 0
        with self.assertRaises(ChordTestError):
            assert chord.check_printed_duration()
        chord.tuplet = Tuplet(3, 2)
        assert chord.check_printed_duration()
        chord.type = 'quarter'
        with self.assertRaises(ChordTestError):
            assert chord.check_printed_duration()
