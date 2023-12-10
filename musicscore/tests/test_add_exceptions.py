from musicscore import Part, Chord, Measure, Beat, Voice, Score, Staff, Accidental
from musicscore.exceptions import AlreadyFinalizedError, AddChordError
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLCoda, XMLSegno


class TestAddExceptions(IdTestCase):
    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p1')
        self.measure = self.part.add_measure()
        self.staff = self.measure.add_staff()
        self.voice = self.staff.add_voice()
        self.beat = self.voice.add_beat()

    def test_add_chord_to_part(self):
        p = Part(id='part-1')
        p.add_chord(Chord(60, 4))
        p.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            p.add_chord(Chord(60, 4))

    def test_add_child_to_part(self):
        p = Part(id='part-1')
        p.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            p.add_child(Measure(1))

    def test_add_measure_to_part(self):
        p = Part(id='part-1')
        p.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            p.add_measure()

    def test_add_direction_type_to_chord(self):
        p = Part(id='part-1')
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.add_direction_type(XMLCoda())
        ch.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            ch.add_direction_type(XMLSegno())

    def test_add_midi_to_chord(self):
        p = Part(id='part-1')
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.add_midi(63)
        assert [m.value for m in ch.midis] == [60, 63]
        ch.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            ch.add_midi(65)

    def test_add_dynamics_to_chord(self):
        p = Part(id='part-1')
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.add_dynamics('ff')
        ch.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            ch.add_dynamics('pp')

    def test_add_tie_to_chord(self):
        ch = Chord([60, 62], 4)
        self.part.add_chord(ch)
        ch.add_tie('start')
        ch.finalize()
        for note in ch.notes:
            assert note.is_tied_to_next
            assert not note.is_tied_to_previous
        ch.add_tie('stop')
        for note in ch.notes:
            assert note.is_tied_to_next
            assert note.is_tied_to_previous

    def test_add_lyric_to_chord(self):
        p = Part(id='part-1')
        ch = Chord(60, 1)
        p.add_chord(ch)
        lyrics1 = ch.add_lyric('one')
        lyrics2 = ch.add_lyric('two')
        ch.finalize()
        assert ch.notes[0].find_children('XMLLyric') == [lyrics1, lyrics2]

    def test_add_wedge_to_chord(self):
        p = Part(id='part-1')
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.add_wedge('crescendo')
        ch.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            ch.add_wedge('stop')

    def test_add_child_to_measure(self):
        self.measure.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.measure.add_child(Staff())

    def test_add_staff_to_measure(self):
        self.measure.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.measure.add_staff()

    def test_add_voice_to_measure(self):
        self.measure.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.measure.add_voice()

    def test_add_child_to_beat(self):
        self.beat.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.beat.add_child(Chord(60, 1))

    def test_add_chord_to_beat(self):
        self.beat.finalize()
        with self.assertRaises(AddChordError):
            self.beat.add_chord(Chord(60, 4))

    def test_add_child_to_midi(self):
        ch = Chord(60, 1)
        self.part.add_chord(ch)
        ch.midis[0].add_child(Accidental())
        ch.number_of_dots = 1
        ch.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            ch.midis[0].add_child(Accidental())

    def test_add_tie_to_midi(self):
        ch = Chord([60, 62], 4)
        self.part.add_chord(ch)
        ch.midis[0].add_tie('start')
        ch.finalize()
        n1, n2 = ch.notes
        assert n1.is_tied_to_next
        assert not n1.is_tied_to_previous
        assert not n2.is_tied_to_next
        assert not n2.is_tied_to_previous
        ch.midis[0].add_tie('stop')
        assert n1.is_tied_to_next
        assert n1.is_tied_to_previous
        assert not n2.is_tied_to_next
        assert not n2.is_tied_to_previous

    def test_add_child_to_score(self):
        self.score.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.score.add_child(Part('p2'))

    def test_add_part_to_score(self):
        self.score.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.score.add_part('p2')

    def test_add_child_to_staff(self):
        self.staff.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.staff.add_child(Voice())

    def test_add_voice_to_staff(self):
        self.staff.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.staff.add_voice()

    def test_add_child_to_voice(self):
        self.voice.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.voice.add_child(Beat(1))

    def test_add_chord_to_voice(self):
        self.voice.finalize()
        with self.assertRaises(AddChordError):
            self.voice.add_chord(Chord(60, 1))

    def test_add_beat_to_voice(self):
        self.voice.finalize()
        with self.assertRaises(AlreadyFinalizedError):
            self.voice.add_beat(1)
