import inspect

from musicscore import Part, Chord, Score, beam_chord_group
from musicscore.tests.util import IdTestCase, generate_path


class TestBeams(IdTestCase):
    def test_beams_example(self):
        score = Score()
        p = score.add_part('p1')
        p.add_measure([1, 4])
        for qd in 7 * 4 * [1 / 4]:
            p.add_chord(Chord(71, qd))
        for l in [[0, 71, 71, 71],
                  [0, 71, 71, 0],
                  [71, 0, 71, 71],
                  [71, 71, 0, 71],
                  [71, 0, 0, 71],
                  [71, 0, 0, 71],
                  [71, 0, 71, 0, 71],
                  [71, 0, 71, 0, 71, 71],
                  [71, 0, 0, 71, 71, 71, 71, 71]]:
            for m in l:
                p.add_chord(Chord(m, 1 / len(l)))
        for i in range(1, len(p.get_children()) // 4):
            p.get_measure(i * 4 + 1).new_system = True
        m = p.get_measure(2)
        for chord in m.get_chords():
            chord.beams = None
        m = p.get_measure(3)
        chords = m.get_chords()
        chords[0].beams = {1: 'begin', 2: 'begin'}
        chords[1].beams = {1: 'continue', 2: 'continue'}
        chords[2].beams = {1: 'end', 2: 'end'}
        chords[3].beams = None
        m = p.get_measure(4)
        chords = m.get_chords()
        chords[0].beams = None
        chords[1].beams = {1: 'begin', 2: 'begin'}
        chords[2].beams = {1: 'continue', 2: 'continue'}
        chords[3].beams = {1: 'end', 2: 'end'}
        m = p.get_measure(5)
        beat = m.get_beats()[0]
        beat._update_chord_types()
        chords = beat.get_chords()
        beam_chord_group(chords[:2])
        beam_chord_group(chords[2:])

        m = p.get_measure(6)
        beat = m.get_beats()[0]
        beat._update_chord_types()
        chords = beat.get_chords()
        beam_chord_group(chords[:2])
        for chord in chords[2:]:
            chord.beams = None

        m = p.get_measure(7)
        beat = m.get_beats()[0]
        beat._update_chord_types()
        chords = beat.get_chords()
        beam_chord_group(chords[:2])
        beam_chord_group(chords[2:])
        chords[1].beams[1] = 'continue'
        chords[2].beams[1] = 'continue'

        m = p.get_measure(13)
        chords = m.get_chords()
        chords[0].beams = None
        chords[-1].beams = None

        path = generate_path(inspect.currentframe())
        score.export_xml(path)
