"""
Tempo Markings: note=bpm, text (note=bpm), note=note, (note=note), (note=bpm)
"""
from pathlib import Path

from musictree import Score

score = Score()
part = score.add_part('p1')


xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
