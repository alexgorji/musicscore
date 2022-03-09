from quicktions import Fraction

from musictree.accidental import Accidental
from musictree.beat import Beat
from musictree.chord import Chord, split_copy, group_chords
from musictree.exceptions import ChordHasNoParentError, ChordQuarterDurationAlreadySetError
from musictree.measure import Measure
from musictree.midi import Midi
from musictree.quarterduration import QuarterDuration
from musictree.tests.util import check_notes, ChordTestCase, create_articulation, create_technical
from musictree.util import XML_ARTICULATION_CLASSES, XML_TECHNICAL_CLASSES
from musicxml.xmlelement.xmlelement import *


def get_chord_midi_values(chord):
    return [m.value for m in chord._midis]


class TestTreeChord(ChordTestCase):

    def test_mocks(self):
        assert self.mock_voice.number == 1
        assert self.mock_beat.up.number == 1
        ch = Chord()
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
        assert get_chord_midi_values(ch) == [70, 50]
        ch = Chord(0, 1)
        assert get_chord_midi_values(ch) == [0]
        ch = Chord(Midi(90, accidental=Accidental(mode='enharmonic_1')), 1)
        assert get_chord_midi_values(ch) == [90]
        ch = Chord([Midi(90, accidental=Accidental(mode='enharmonic_1')), 70], 1)
        assert get_chord_midi_values(ch) == [90, 70]

        with self.assertRaises(ValueError):
            Chord([0, 60], 1)

        """
        A grace note cannot be a rest.
        """
        with self.assertRaises(ValueError):
            Chord(0, 0)

    def test_chord_needs_parent_error(self):
        ch = Chord(70, 1)
        with self.assertRaises(ChordHasNoParentError):
            ch.final_updates()
        ch._parent = self.mock_beat
        ch.final_updates()

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
        c.final_updates()
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
        c.final_updates()
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
        # c.final_updates()

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
        c.final_updates()
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
        c.quarter_duration = 0
        c._parent = self.mock_beat
        c.final_updates()
        expected = """<note>
  <grace />
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <voice>1</voice>
</note>
"""
        assert c.notes[0].to_string() == expected
        # change chord's attributes?
        c.notes[0].relative_x = 20
        c.notes[0].relative_y = 15
        expected = """<note relative-x="20" relative-y="15">
  <grace />
  <pitch>
    <step>C</step>
    <octave>4</octave>
  </pitch>
  <voice>1</voice>
</note>
"""
        assert c.notes[0].to_string() == expected

    def test_chord_single_non_rest(self):
        """
        Test a chord with a non rest single midi
        """
        c = Chord(72, 2)
        c.midis[0].accidental.show = True
        c._parent = self.mock_beat
        c.final_updates()

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
        # c.final_updates()
        assert c.notes[0].xml_pitch is None
        assert c.notes[0].xml_rest is not None
        assert c.is_rest

    def test_chord_single_non_rest_midi_with_accidental(self):
        """
        Test chord with a non rest single midi with accidental set.
        """
        chord = Chord(Midi(70, accidental=Accidental(mode='sharp')), 1)
        chord._parent = self.mock_beat
        chord.final_updates()
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
        expected = """<note>
  <rest />
  <duration>2</duration>
  <voice>1</voice>
  <type>half</type>
</note>
"""
        chord.final_updates()
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
        chord.final_updates()
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
        chord.final_updates()
        chord.xml_stem = 'up'
        expected_1 = """<note>
  <chord />
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

    def test_split_copy(self):
        ch = Chord(midis=[Midi(61, accidental=Accidental(mode='sharp'))], quarter_duration=2, offset=0.5)
        copied = split_copy(ch)
        assert ch.midis != copied.midis
        assert ch.midis[0].value == copied.midis[0].value
        assert ch.midis[0].accidental != copied.midis[0].accidental
        assert ch.midis[0].accidental.mode == copied.midis[0].accidental.mode
        copied.midis[0].accidental.show = False
        assert ch.midis[0].accidental.show is None
        assert copied.midis[0].accidental.show is False

    def test_split_tied_copy(self):
        ch = Chord(midis=60, quarter_duration=1)
        copied = split_copy(ch)
        assert ch._ties == copied._ties == []

    def test_split_quarter_durations(self):
        ch = Chord(midis=60, quarter_duration=4)
        copied = split_copy(ch)
        assert id(ch.quarter_duration) != id(copied.quarter_duration)
        ch.quarter_duration = 2
        assert copied.quarter_duration == 4
        assert ch.quarter_duration == 2

        ch = Chord(midis=60, quarter_duration=5)
        beats = [Beat(1), Beat(1), Beat(1), Beat(1)]
        quarter_durations = ch.quarter_duration.get_beatwise_sections(beats=beats)
        ch.quarter_duration = quarter_durations[0][0]
        copied = split_copy(ch, quarter_durations[1])
        assert [ch.quarter_duration, copied.quarter_duration] == [4, 1]

    def test_chord_tie_untie(self):
        ch1 = Chord(midis=[60, 61], quarter_duration=1)
        ch2 = Chord(midis=[60, 61], quarter_duration=1)
        ch1.add_tie('start')
        ch2.add_tie('stop')
        ch1._parent = self.mock_beat
        ch2._parent = self.mock_beat
        ch1.final_updates()
        ch2.final_updates()
        assert [n.is_tied for n in ch1.notes] == [True, True]
        assert [n.is_tied for n in ch2.notes] == [False, False]
        assert [n.is_tied_to_previous for n in ch2.notes] == [True, True]

        ch1 = Chord(midis=[60, 61], quarter_duration=1)
        ch2 = Chord(midis=[60, 61], quarter_duration=1)
        ch1._parent = self.mock_beat
        ch2._parent = self.mock_beat
        ch1.final_updates()
        ch2.final_updates()

        ch1.add_tie('start')
        ch2.add_tie('stop')

        assert [n.is_tied for n in ch1.notes] == [True, True]
        assert [n.is_tied for n in ch2.notes] == [False, False]
        assert [n.is_tied_to_previous for n in ch2.notes] == [True, True]

    def test_group_chords(self):
        chords = [Chord(60, qd) for qd in [1 / 6, 1 / 6, 1 / 6, 1 / 10, 3 / 10, 1 / 10]]
        with self.assertRaises(ValueError):
            assert group_chords(chords, [1 / 2, 1 / 2, 1 / 2])
        assert group_chords(chords, [1 / 2, 1 / 2]) == [chords[:3], chords[3:]]
        assert group_chords(chords, [1 / 3, 2 / 3]) == [chords[:2], chords[2:]]
        assert group_chords(chords, [1 / 4, 3 / 4]) is None

    def test_has_same_pitches(self):
        ch1 = Chord([60, Midi(61, accidental=Accidental(show=True)), 62], 1)
        ch2 = Chord([60, Midi(61, accidental=Accidental(show=True))], 1)
        assert not ch1.has_same_pitches(ch2)
        ch2 = Chord([60, Midi(61, accidental=Accidental(show=True)), 62], 1)
        assert ch1.has_same_pitches(ch2)
        ch2 = Chord([60, Midi(61, accidental=Accidental(show=False)), 62], 1)
        assert not ch1.has_same_pitches(ch2)
        ch2 = Chord([60, Midi(61, accidental=Accidental(show=True, mode='flat')), 62], 1)
        assert not ch1.has_same_pitches(ch2)

    def test_add_lyric(self):
        ch = Chord(60, 2)
        ch._parent = self.mock_beat
        ch.add_lyric('test')
        ch.final_updates()
        assert ch.notes[0].xml_lyric is not None
        assert ch.notes[0].xml_lyric.xml_text.value_ == 'test'

    def test_add_lyrics_after_creating_notes(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        lyrics1 = ch.add_lyric('one')
        ch.final_updates()
        lyrics2 = ch.add_lyric('two')
        assert ch.notes[0].find_children('XMLLyric') == [lyrics1, lyrics2]

    def test_get_staff_number(self):
        ch = Chord(60, 2)
        ch._parent = self.mock_beat
        assert ch.get_staff_number() is None
        self.mock_staff.number = 1
        assert ch.get_staff_number() == 1

    def test_add_technicals(self):
        for technical_class in XML_TECHNICAL_CLASSES:
            ch = Chord(60, 1)
            ch._parent = self.mock_beat
            ch.add_xml_technical(create_technical(technical_class))
            ch.final_updates()
            assert ch.notes[0].xml_notations.xml_technical.get_children()[0].__class__ == technical_class

    #
    # def test_technical_fret(self):
    #     ch = Chord(60, 1)
    #     ch._parent = self.mock_beat
    #     ch.add_xml_technical(XMLFret())

    def test_add_articulations(self):
        for articulation_class in XML_ARTICULATION_CLASSES:
            ch = Chord(60, 1)
            ch._parent = self.mock_beat
            ch.add_xml_articulation(create_articulation(articulation_class))
            ch.final_updates()
            assert ch.notes[0].xml_notations.xml_articulations.get_children()[0].__class__ == articulation_class

    def test_add_articulation_after_creating_notes(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        staccato = ch.add_xml_articulation(create_articulation(XMLStaccato))
        ch.final_updates()
        assert isinstance(ch.notes[0].xml_notations.xml_articulations.get_children()[0], XMLStaccato)
        accent = ch.add_xml_articulation(create_articulation(XMLAccent))
        assert ch.notes[0].xml_notations.xml_articulations.get_children() == [staccato, accent]

    def test_add_multiple_articulations(self):
        articulation_classes = XML_ARTICULATION_CLASSES[:3]
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        for a in articulation_classes:
            ch.add_xml_articulation(a())
        assert len(ch._xml_articulations) == 3
        ch.final_updates()
        n = ch.notes[0]
        assert n.xml_notations.xml_articulations is not None
        assert [type(a) for a in n.xml_notations.xml_articulations.get_children()] == articulation_classes

    def test_add_ornaments(self):
        self.fail('Incomplete')

    def test_add_wedge(self):
        self.fail('Incomplete')

    def test_add_words(self):
        self.fail('Incomplete')

    def test_add_clef(self):
        self.fail('Incomplete')

    def test_add_bracket(self):
        self.fail('Incomplete')

    def test_add_grace_chords(self):
        self.fail('Incomplete')

    def test_add_slur(self):
        self.fail('Incomplete')

    def test_add_slide(self):
        self.fail('Incomplete')

    def test_add_fermata(self):
        self.fail('Incomplete')

    def test_percussion_notation(self):
        self.fail('Incomplete')

    def test_finger_tremolo(self):
        self.fail('Incomplete')
