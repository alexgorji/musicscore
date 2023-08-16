from pathlib import Path

from musictree.beat import Beat
from musictree.chord import Chord
from musictree.measure import Measure
from musictree.part import Part
from musictree.score import Score
from musictree.staff import Staff
from musictree.voice import Voice

# from musictree import *

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
Add a measure:
"""
m = p.add_child(Measure(number=1))
"""
Add a staff:
"""
st = m.add_child(Staff(number=1))
"""
Add a voice:
"""
v = st.add_child(Voice(number=1))
"""
Add beats:
"""
for _ in range(4):
    v.add_child(Beat(quarter_duration=1))
"""
Select first beat
"""
beat = v.get_children()[0]
"""
Add a chord:
"""
beat.add_child(Chord(60, 4))

"""
... and export
"""
xml_path = Path(__file__).with_suffix('.xml')
s.export_xml(xml_path)