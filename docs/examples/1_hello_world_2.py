from pathlib import Path

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.staff import Staff
from musictree.voice import Voice

"""
Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
"""
"""
Create a score:
"""
s = Score()
"""
Add a part:
"""
p = s.add_child(Part('P1', name='Part 1'))
"""
Add directly a chord to part
"""
p.add_chord(Chord(60, 4))
"""
... and export
"""
xml_path = Path(__file__).with_suffix('.xml')
s.export_xml(xml_path)