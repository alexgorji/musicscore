from pathlib import Path

from musictree import Score, G, A, B, C, D, E, F, Chord, Midi, Accidental

"""
All pitches from c4 to c5 in ascending quarter steps; different Accidental.mode: standard, enharmonic, sharp, 
flat, force-sharp, force-flat. 
"""


def create_part(mode):
    scale = [Midi(m / 2) for m in range(120, 144)]
    p = score.add_part(f'{mode}')
    p.name = f'mode {mode}'
    for m in scale:
        m.accidental.mode = mode
        ch = Chord(m, 1)
        p.add_chord(ch)


score = Score('Accidental modes')
for mode in ['standard', 'enharmonic', 'sharp', 'flat', 'force-sharp', 'force-flat']:
    create_part(mode)

xml_path = Path(__file__).with_suffix('.xml')
score.export_xml(xml_path)
