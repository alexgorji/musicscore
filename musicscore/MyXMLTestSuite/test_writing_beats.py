from musicscore import Beat, Chord, Part
from musicscore.tests.util import IdTestCase


class TestWritingBeats(IdTestCase):
    def test_writing_32nds(self):
        # 1, 5, 2
        values = [1, 5, 2]
        unit = 8
        chords = [Chord(60, v / unit) for v in values]
        p = Part(id='p1')
        m = p.add_measure([1, 4])
        [p.add_chord(ch) for ch in chords]
        beat = m.get_beats()[0]
        assert beat.get_chords() == chords
        assert chords[1].quarter_duration == 5 / 8
        m.finalize()
        # After finalizing the qd of the second chord has been changed:
        assert chords[1].quarter_duration == 3 / 8
        # This is because 5/8 qd is not writable and has been split in two qds: 3/8 + 2/8.  It means a chord has
        # been added to the beat after the second chord qd of which has been changed too.
        assert [ch.quarter_duration for ch in beat.get_chords()] == [1 / 8, 3 / 8, 2 / 8, 2 / 8]
        # Be aware now that chords and beat.get_chords() diverged
        assert beat.get_chords() != chords
        # and the second chord is not copied but has destructively changed its qd:
        assert [ch.quarter_duration for ch in chords] == [1 / 8, 3 / 8, 2 / 8]
        assert sum([ch.quarter_duration for ch in chords]) != 1
        # Of course there the spit chords are tied:
        assert beat.get_chords()[1].is_tied_to_next
        assert beat.get_chords()[2].is_tied_to_previous
        # Which quarter durations (at which position are not writable
        # The type of each chord is (at the moment) set on its Note children via QuarterDuration.
        print([ch.type for ch in chords])
