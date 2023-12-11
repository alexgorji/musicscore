from unittest import TestCase

from quicktions import Fraction

from musicscore import Part, Time
from musicscore.chord import Chord
from musicscore.measure import Measure
from musicscore.tests.test_beat import create_voice
from musicscore.tests.util import IdTestCase
from musicscore.tests.util_subdivisions import generate_all_quintuplets_manually, generate_all_sextuplets_manually, \
    generate_all_triplets_manually


class TestTuplets(IdTestCase):

    def test_simple_triplet(self):
        expected_1 = """<note>
    <pitch>
      <step>C</step>
      <octave>4</octave>
    </pitch>
    <duration>1</duration>
    <voice>1</voice>
    <type>eighth</type>
    <time-modification>
      <actual-notes>3</actual-notes>
      <normal-notes>2</normal-notes>
      <normal-type>eighth</normal-type>
    </time-modification>
    <notations>
      <tuplet type="start" number="1" bracket="yes" />
    </notations>
  </note>
"""
        expected_2 = """<note>
    <pitch>
      <step>C</step>
      <octave>4</octave>
    </pitch>
    <duration>2</duration>
    <voice>1</voice>
    <type>quarter</type>
    <time-modification>
      <actual-notes>3</actual-notes>
      <normal-notes>2</normal-notes>
      <normal-type>eighth</normal-type>
    </time-modification>
    <notations>
      <tuplet type="stop" number="1" />
    </notations>
  </note>
"""
        m = Measure(1)
        ch1 = Chord(midis=60, quarter_duration=1 / 3)
        ch2 = Chord(midis=60, quarter_duration=2 / 3)
        for c in [ch1, ch2]:
            c.midis[0].accidental.show = False
            m._add_chord(c)
        m.finalize()
        assert ch1.notes[0].to_string() == expected_1
        assert ch2.notes[0].to_string() == expected_2

    def test_chord_simple_triplet(self):
        m = Measure(1)
        chords = [Chord(60, 1 / 3), Chord(61, 2 / 3)]

        for x in chords:
            m._add_chord(x)

        m.finalize()

        t1, t2 = [ch.notes[0].xml_notations.xml_tuplet for ch in chords]
        assert t1.type == 'start'
        assert t2.type == 'stop'
        for note in [ch.notes[0] for ch in chords]:
            assert note.xml_time_modification is not None
            assert note.xml_time_modification.xml_actual_notes.value_ == 3
            assert note.xml_time_modification.xml_normal_notes.value_ == 2
            assert note.xml_time_modification.xml_normal_type.value_ == 'eighth'

    def test_chord_quintuplet(self):
        measures = []
        for index, quintuplet in enumerate(generate_all_quintuplets_manually()):
            m = Measure(index + 1)
            for q in quintuplet:
                m._add_chord(Chord(midis=60, quarter_duration=q))
            m.finalize()
            measures.append(m)

        for m in measures:
            chords = [chord for chord in m.get_chords() if not chord.is_rest]
            for ch in chords:
                note = ch.notes[0]
                assert note.xml_time_modification is not None
                assert note.xml_time_modification.xml_actual_notes.value_ == 5
                assert note.xml_time_modification.xml_normal_notes.value_ == 4
                assert note.xml_time_modification.xml_normal_type.value_ == '16th'
            first_note = chords[0].notes[0]
            last_note = chords[-1].notes[0]
            t1, t2 = first_note.xml_notations.xml_tuplet, last_note.xml_notations.xml_tuplet
            assert t1.type == 'start'
            assert t2.type == 'stop'

    def test_chord_sextuplets_not_writable_1(self):
        m1 = Measure(1)
        quarter_durations = [Fraction(1, 6), Fraction(5, 6)]
        for q in quarter_durations:
            m1._add_chord(Chord(midis=60, quarter_duration=q))
        m1._split_not_writable_chords()
        m1.finalize()
        b = m1.get_voice(staff_number=1, voice_number=1).get_children()[0]
        assert b.get_children() == m1.get_chords()[:3]
        n1, n2, n3 = [ch.notes[0] for ch in m1.get_chords()[:3]]
        # print([n.quarter_duration for n in [n1, n2, n3]])
        assert n1.xml_notations.xml_tuplet.type == 'start'
        assert n3.xml_notations.xml_tuplet.type == 'stop'
        assert not n1.is_tied
        assert n2.is_tied
        assert n3.is_tied_to_previous
        assert n3.xml_dot is not None
        assert n3.midi.accidental.show is False

    def test_chord_sextuplets_not_writable_2(self):
        m1 = Measure(1)
        quarter_durations = [Fraction(5, 6), Fraction(1, 6)]
        for q in quarter_durations:
            m1._add_chord(Chord(midis=60, quarter_duration=q))
        m1._split_not_writable_chords()
        m1.finalize()
        n1, n2, n3 = [ch.notes[0] for ch in m1.get_chords()[:3]]
        assert n1.xml_notations.xml_tuplet.type == 'start'
        assert n3.xml_notations.xml_tuplet.type == 'stop'
        assert n1.is_tied
        assert n2.is_tied_to_previous
        assert not n3.is_tied
        assert n1.xml_dot is not None
        assert n2.midi.accidental.show is False

    def test_chord_sextuplets(self):
        measures = []
        for index, sextuplet in enumerate(generate_all_sextuplets_manually()):
            m = Measure(index + 1)
            for q in sextuplet:
                m._add_chord(Chord(midis=60, quarter_duration=q))
            m._split_not_writable_chords()
            m.finalize()
            measures.append(m)

        for m in measures:
            chords = [chord for chord in m.get_chords() if not chord.is_rest]
            for ch in chords:
                note = ch.notes[0]
                assert note.xml_time_modification is not None
                assert note.xml_time_modification.xml_actual_notes.value_ == 6
                assert note.xml_time_modification.xml_normal_notes.value_ == 4
                assert note.xml_time_modification.xml_normal_type.value_ == '16th'
            first_note = chords[0].notes[0]
            last_note = chords[-1].notes[0]
            t1, t2 = first_note.xml_notations.xml_tuplet, last_note.xml_notations.xml_tuplet
            assert t1.type == 'start'
            assert t2.type == 'stop'

    def test_update_xml_brackets(self):
        v1 = create_voice()
        beats = v1.update_beats(1, 1, 1, 1)
        ch1, ch2, ch3 = chords = [Chord(60, 2 / 5), Chord(61, 2 / 5), Chord(62, 1 / 5)]
        for ch in chords:
            beats[0].add_child(ch)
        v1.up.up._update_divisions()
        beats[0].finalize()
        assert ch1.notes[0].xml_notations.xml_tuplet.type == 'start'
        assert ch1.notes[0].xml_notations.xml_tuplet.bracket == 'yes'
        assert ch1.notes[0].xml_notations.xml_tuplet.number == 1
        assert ch2.notes[0].xml_notations is None
        assert ch3.notes[0].xml_notations.xml_tuplet.type == 'stop'
        assert ch3.notes[0].xml_notations.xml_tuplet.number == 1

    def test_complex_tuplet(self):
        v1 = create_voice()
        beats = v1.update_beats(1)
        for quarter_duration in [1 / 6, 1 / 6, 1 / 6, 1 / 10, 3 / 10, 1 / 10]:
            v1._add_chord(Chord(60, quarter_duration))
        v1.up.up._update_divisions()
        beats[0].finalize()
        n1, n2, n3, n4, n5, n6 = [ch.notes[0] for ch in v1.get_chords()]
        for n in [n1, n2, n3]:
            assert (n.xml_time_modification.xml_actual_notes.value_, n.xml_time_modification.xml_normal_notes.value_,
                    n.xml_time_modification.xml_normal_type.value_) == (3, 2, '16th')
        for n in [n4, n5, n6]:
            assert (n.xml_time_modification.xml_actual_notes.value_, n.xml_time_modification.xml_normal_notes.value_,
                    n.xml_time_modification.xml_normal_type.value_) == (5, 4, '32nd')
        assert n1.xml_notations.xml_tuplet.type == 'start'
        assert n2.xml_notations is None
        assert n3.xml_notations.xml_tuplet.type == 'stop'
        assert n4.xml_notations.xml_tuplet.type == 'start'
        assert n5.xml_notations is None
        assert n6.xml_notations.xml_tuplet.type == 'stop'

    def test_group_beams_triplets(self):
        v1 = create_voice()
        beats = v1.update_beats(1, 1, 1)
        for quarter_duration in [q for group in generate_all_triplets_manually() for q in group]:
            v1._add_chord(Chord(60, quarter_duration))
        v1.up.up._update_divisions()
        for index, beat in enumerate(beats):
            beat.finalize()
            if index == 0:
                for i, c in enumerate(beat.get_children()):
                    beams = c.notes[0].find_children('XMLBeam')
                    assert len(beams) == 1
                    assert beams[0].number == 1
                    assert beams[0].value_ == 'begin' if i == 0 else 'continue' if i == 1 else 'end'
            else:
                for c in beat.get_children():
                    assert c.notes[0].find_child('XMLBeam') is None

    def test_quarter_triplets(self):
        m = Measure(1)
        m.time = Time(3, 2)
        quarter_durations = [2 / 3, 4 / 3, 4 / 3, 2 / 3, 2 / 3, 2 / 3, 2 / 3]
        chords = [Chord(60 + i, qd) for i, qd in enumerate(quarter_durations)]
        [m._add_chord(chord) for chord in chords]
        m.finalize()

        # check durations
        notes = [ch.notes[0] for ch in chords]
        divisions = m.xml_object.xml_attributes.xml_divisions.value_
        assert divisions == 3
        assert [n.xml_duration.value_ for n in notes] == [qd * divisions for qd in quarter_durations]

        # check note types
        assert [n.xml_type.value_ for n in notes] == ['quarter', 'half', 'half',
                                                      'quarter', 'quarter', 'quarter', 'quarter']
        # check time modifications
        """
        <time-modification>
          <actual-notes>3</actual-notes>
          <normal-notes>2</normal-notes>
          <normal-type>quarter</normal-type>
        </time-modification>
        """
        for n in notes:
            assert (n.xml_time_modification.xml_actual_notes.value_, n.xml_time_modification.xml_normal_notes.value_,
                    n.xml_time_modification.xml_normal_type.value_) == (3, 2, 'quarter')

        # check brackets
        """
        <notations>
            <tuplet bracket="yes" number="1" type="start" />
        </notations>
        
        <notations>
            <tuplet number="1" type="stop" />
        </notations>
        """
        for i, n in enumerate(notes):
            if i in [0, 2, 4]:
                tuplet = n.xml_notations.xml_tuplet
                assert tuplet.bracket == 'yes'
                assert tuplet.type == 'start'
            elif i in [1, 3, 6]:
                tuplet = n.xml_notations.xml_tuplet
                assert tuplet.type == 'stop'
            else:
                assert not n.xml_notations

    def test_quarter_triplets_with_actual_signatures(self):
        m = Measure(1)
        m.time = Time(6, 4)
        m.time.actual_signatures = [1, 2, 1, 2, 1, 2]
        quarter_durations = [2 / 3, 4 / 3, 4 / 3, 2 / 3, 2 / 3, 2 / 3, 2 / 3]
        chords = [Chord(60 + i, qd) for i, qd in enumerate(quarter_durations)]
        [m._add_chord(chord) for chord in chords]
        m.finalize()

        # check durations
        notes = [ch.notes[0] for ch in chords]
        divisions = m.xml_object.xml_attributes.xml_divisions.value_
        assert divisions == 3
        assert [n.xml_duration.value_ for n in notes] == [qd * divisions for qd in quarter_durations]

        # check note types
        assert [n.xml_type.value_ for n in notes] == ['quarter', 'half', 'half',
                                                      'quarter', 'quarter', 'quarter', 'quarter']
        # check time modifications
        """
        <time-modification>
          <actual-notes>3</actual-notes>
          <normal-notes>2</normal-notes>
          <normal-type>quarter</normal-type>
        </time-modification>
        """
        for n in notes:
            assert (n.xml_time_modification.xml_actual_notes.value_, n.xml_time_modification.xml_normal_notes.value_,
                    n.xml_time_modification.xml_normal_type.value_) == (3, 2, 'quarter')

        # check brackets
        """
        <notations>
            <tuplet bracket="yes" number="1" type="start" />
        </notations>

        <notations>
            <tuplet number="1" type="stop" />
        </notations>
        """
        for i, n in enumerate(notes):
            if i in [0, 2, 4]:
                tuplet = n.xml_notations.xml_tuplet
                assert tuplet.bracket == 'yes'
                assert tuplet.type == 'start'
            elif i in [1, 3, 6]:
                tuplet = n.xml_notations.xml_tuplet
                assert tuplet.type == 'stop'
            else:
                assert not n.xml_notations
