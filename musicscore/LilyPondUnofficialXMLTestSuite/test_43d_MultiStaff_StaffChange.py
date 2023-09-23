"""
Staff changes in a piano staff. The voice from the second staff has some notes/chords on the first staff. The
final two chords have some notes on the first, some on the second staff.
"""
from pathlib import Path

from musicscore import Score, Chord, C, A, E, Time, G
from musicscore.tests.util import IdTestCase


class TestLily43a(IdTestCase):
    def test_lily_43a_MultiStaff_StaffChange(self):
        score = Score()
        part = score.add_part('p1')
        t = Time(4, 4)
        t.actual_signatures = [1, 2, 1, 2]
        part.add_measure(time=t)

        part.add_chord(Chord(0, 4), staff_number=1, voice_number=1)

        for index, m in enumerate([A(3), E(4), A(3), E(4), C(5), E(4), A(3), A(4)]):
            if index in [1, 3, 4, 5]:
                m.set_staff_number(1)
            part.add_chord(Chord(m, 0.5), staff_number=2, voice_number=1)

        part.add_chord(Chord(0, 4), staff_number=1, voice_number=1)
        for index, m in enumerate([
            [C(3), E(3), G(3), C(4)],
            [C(4), E(4), G(4)],
            [C(3), E(3), G(3), C(4)],
            [G(3), C(4), E(4), G(4)]
        ]):
            if index in [1]:
                for x in m:
                    x.set_staff_number(1)
            part.add_chord(Chord(m, 0.5), staff_number=2, voice_number=1)

        part.add_chord(Chord(0, 2), staff_number=2)
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
