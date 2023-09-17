"""Several spanners defined in MusicXML: tuplet, slur (solid, dashed), tie, wedge (cresc, dim), tr + wavy-line,
single-note trill spanner, octave-shift (8va,15mb), bracket (solid down/down, dashed down/down, solid none/down,
dashed none/up, solid none/none), dashes, glissando (wavy), bend-alter, slide (solid), grouping, two-note tremolo,
hammer-on, pull-off, pedal (down, change, up)."""
from pathlib import Path

from musictree import Score, Time, Chord
from musictree.tests.util import IdTestCase
from musictree.util import slur_chords, wedge_chords, trill_chords, bracket_chords
from musicxml import XMLBracket


class TestLily33a(IdTestCase):
    def test_lily_33a_Spanners(self):
        score = Score()
        part = score.add_part('p1')

        t = Time(3, 4)
        t.actual_signatures = [1, 2, 1, 4]
        part.add_measure(t)
        part.add_measure(Time(3, 4))

        [part.add_chord(Chord(71, 2 / 3)) for _ in range(3)]
        part.add_chord(Chord(0, 1))

        chords = [Chord(71, 1) for _ in range(3)]
        slur_chords(chords)
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        slur_chords(chords, line_type='dashed')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        wedge_chords(chords, 'crescendo', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        wedge_chords(chords, 'diminuendo', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        trill_chords(chords, placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1), Chord(0, 2)]
        trill_chords(chords, placement='above')
        [part.add_chord(ch) for ch in chords]

        # chords = [Chord(71, 1) for _ in range(3)]
        # octave_chords(chords, placement='above')
        # [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        bracket_chords(chords, 'solid', 'down', 'down', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        bracket_chords(chords, 'dashed', 'down', 'down', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        bracket_chords(chords, 'solid', 'none', 'down', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        bracket_chords(chords, 'dashed', 'none', 'up', placement='above')
        [part.add_chord(ch) for ch in chords]

        chords = [Chord(71, 1) for _ in range(3)]
        bracket_chords(chords, 'solid', 'none', 'none', placement='above')
        [part.add_chord(ch) for ch in chords]

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
