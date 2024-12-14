from pathlib import Path

from musicscore.beat import Beat
from musicscore.chord import Chord
from musicscore.measure import Measure
from musicscore.part import Part
from musicscore.score import Score
from musicscore.staff import Staff
from musicscore.voice import Voice

# from musicscore import *

"""
Hello World as musicxml means having a C4 pitch as a whole in a 4/4 measure with treble clef.
"""
"""
Create a score:
"""
s = Score(title="Hello World 1")
"""
Add a part:
"""
p = s.add_child(Part("hw1", name="HW1"))
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
xml_path = Path(__file__).with_suffix(".xml")
s.export_xml(xml_path)
