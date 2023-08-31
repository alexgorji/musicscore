"""
Create multiple parts with names
"""
from pathlib import Path

from musictree import Score, Chord

score = Score()
for i in range(5):
    p = score.add_part(f'part-{i}')
    p.add_chord(Chord(0, 4))

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
