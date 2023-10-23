"""
Chords as grace notes.
"""
from pathlib import Path

from musicscore import Score, Chord, A, E, G

score = Score()
part = score.add_part('p1')

chords = [Chord(E(5), 2), Chord(E(5), 2)]
chords[1].add_grace_chord(G(5), type='16th', position='after')
chords[1].add_grace_chord(A(5), type='16th', position='after')

for ch in chords:
    part.add_chord(ch)

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
