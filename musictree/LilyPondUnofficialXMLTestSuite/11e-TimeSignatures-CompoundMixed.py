from pathlib import Path

from musictree import Score, Time, Chord, B

"""
Compound time signatures of mixed type: (3+2)/8+3/4.
"""

score = Score()
part = score.add_part('part')
part.add_measure(time=Time('3+2', 8, 3, 4))
[part.add_chord(Chord(B(4), x / 2)) for x in [1, 1, 1, 1, 1]]
[part.add_chord(Chord(B(4), x)) for x in [1, 1, 1]]

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
