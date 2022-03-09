from unittest import TestCase

from quicktions import Fraction

from musictree.chord import Chord
from musictree.measure import Measure
from musictree.tests.test_beat import create_voice
from musictree.tests.util import generate_all_quintuplets, generate_all_triplets, generate_all_sextuplets


class TestTuplets(TestCase):

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
      <tuplet bracket="yes" number="1" type="start" />
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
      <tuplet number="1" type="stop" />
    </notations>
  </note>
"""
        m = Measure(1)
        ch1 = Chord(midis=60, quarter_duration=1 / 3)
        ch2 = Chord(midis=60, quarter_duration=2 / 3)
        for c in [ch1, ch2]:
            c.midis[0].accidental.show = False
            m.add_chord(c)
        m.final_updates()
        assert ch1.notes[0].to_string() == expected_1
        assert ch2.notes[0].to_string() == expected_2

    def test_chord_simple_triplet(self):
        m = Measure(1)
        chords = [Chord(60, 1 / 3), Chord(61, 2 / 3)]

        for x in chords:
            m.add_chord(x)

        m.final_updates()

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
        for index, quintuplet in enumerate(generate_all_quintuplets()):
            m = Measure(index + 1)
            for q in quintuplet:
                m.add_chord(Chord(midis=60, quarter_duration=q))
            m.final_updates()
            measures.append(m)

        for m in measures:
            for ch in m.get_chords():
                note = ch.notes[0]
                assert note.xml_time_modification is not None
                assert note.xml_time_modification.xml_actual_notes.value_ == 5
                assert note.xml_time_modification.xml_normal_notes.value_ == 4
                assert note.xml_time_modification.xml_normal_type.value_ == '16th'
            first_note = m.get_chords()[0].notes[0]
            last_note = m.get_chords()[-1].notes[0]
            t1, t2 = first_note.xml_notations.xml_tuplet, last_note.xml_notations.xml_tuplet
            assert t1.type == 'start'
            assert t2.type == 'stop'

    def test_chord_sextuplets_not_writable_1(self):
        m1 = Measure(1)
        quarter_durations = [Fraction(1, 6), Fraction(5, 6)]
        for q in quarter_durations:
            m1.add_chord(Chord(midis=60, quarter_duration=q))
        m1.split_not_writable_chords()
        m1.final_updates()
        b = m1.get_voice(staff_number=1, voice_number=1).get_children()[0]
        assert b.get_children() == m1.get_chords()
        n1, n2, n3 = [ch.notes[0] for ch in m1.get_chords()]
        print([n.quarter_duration for n in [n1, n2, n3]])
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
            m1.add_chord(Chord(midis=60, quarter_duration=q))
        m1.split_not_writable_chords()
        m1.final_updates()
        n1, n2, n3 = [ch.notes[0] for ch in m1.get_chords()]
        assert n1.xml_notations.xml_tuplet.type == 'start'
        assert n3.xml_notations.xml_tuplet.type == 'stop'
        assert n1.is_tied
        assert n2.is_tied_to_previous
        assert not n3.is_tied
        assert n1.xml_dot is not None
        assert n2.midi.accidental.show is False

    def test_chord_sextuplets(self):
        measures = []
        for index, sextuplet in enumerate(generate_all_sextuplets()):
            m = Measure(index + 1)
            for q in sextuplet:
                m.add_chord(Chord(midis=60, quarter_duration=q))
            m.split_not_writable_chords()
            m.final_updates()
            measures.append(m)

        for m in measures:
            for ch in m.get_chords():
                note = ch.notes[0]
                assert note.xml_time_modification is not None
                assert note.xml_time_modification.xml_actual_notes.value_ == 6
                assert note.xml_time_modification.xml_normal_notes.value_ == 4
                assert note.xml_time_modification.xml_normal_type.value_ == '16th'
            first_note = m.get_chords()[0].notes[0]
            last_note = m.get_chords()[-1].notes[0]
            t1, t2 = first_note.xml_notations.xml_tuplet, last_note.xml_notations.xml_tuplet
            assert t1.type == 'start'
            assert t2.type == 'stop'

    def test_update_xml_brackets(self):
        v1 = create_voice()
        beats = v1.update_beats(1, 1, 1, 1)
        ch1, ch2, ch3 = chords = [Chord(60, 2 / 5), Chord(61, 2 / 5), Chord(62, 1 / 5)]
        for ch in chords:
            beats[0].add_child(ch)
        v1.up.up.update_divisions()
        beats[0].final_updates()
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
            v1.add_chord(Chord(60, quarter_duration))
        v1.up.up.update_divisions()
        beats[0].final_updates()
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
        for quarter_duration in [q for group in generate_all_triplets() for q in group]:
            v1.add_chord(Chord(60, quarter_duration))
        v1.up.up.update_divisions()
        for index, beat in enumerate(beats):
            beat.final_updates()
            if index == 0:
                for i, c in enumerate(beat.get_children()):
                    beams = c.notes[0].find_children('XMLBeam')
                    assert len(beams) == 1
                    assert beams[0].number == 1
                    assert beams[0].value_ == 'begin' if i == 0 else 'continue' if i == 1 else 'end'
            else:
                for c in beat.get_children():
                    assert c.notes[0].find_child('XMLBeam') is None
