from pathlib import Path

from musictree import Score, G, A, B, C, D, E, F, Chord, Midi, Accidental, Time

"""
All pitch intervals in ascending jump size.
"""

score = Score('Various pitches and interval sizes')
p = score.add_part('intervals')
p.add_measure(Time(2, 4))
for i in range(24):
    m1 = Midi(72 + i)
    m2 = Midi(72 - i)
    p.add_chord(Chord(m1, 1))
    p.add_chord(Chord(m2, 1))

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
