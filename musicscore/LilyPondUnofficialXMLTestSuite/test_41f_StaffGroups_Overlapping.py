"""MusicXML allows for overlapping part-groups, while many applications do not allow overlap- ping groups,
but require them to be properly nested. In this case, one group (within parenthesis) goes from staff 1 to 4 and
another group (also within parenthesis) goes from staff 3 to 5."""
from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase


class TestLily41f(IdTestCase):
    def test_lily_41f_StaffGroupOverlapping(self):
        score = Score()
        parts = [score.add_part(f'p-{i}') for i in range(1, 6)]
        for p in parts:
            p.add_chord(Chord(0, 4))

        score.group_parts(1, 1, 4, name='Group 1', symbol='bracket')
        score.group_parts(2, 3, 4, name='Group 2', symbol='bracket')

        path = Path(__file__).with_suffix('.xml')
        score.export_xml(path)
