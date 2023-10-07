"""
Part names and abbreviations can contain line breaks.
"""

from pathlib import Path

from musicscore import Score, Chord, B
from musicscore.tests.util import IdTestCase


class TestLily413(IdTestCase):
    def test_lily_41e_StaffGroups_InstrumentNames_Linebroken(self):
        score = Score()
        part = score.add_part('p1')
        part.name = """Long
Staff
Name        
"""
        part.abbreviation = """St.
Nm.
"""
        [part.add_chord(Chord(B(4), 4)) for _ in range(23)]
        part.get_measure(6).new_system = True
        part.get_measure(15).new_system = True
        for m in part.get_children()[13:]:
            m.width = 80

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
