from pathlib import Path

from musictree import Score, G, A, B, C, D, E, F, Chord, Midi

"""Accidentals can be cautionary or editorial. Each measure has a normal accidental, an editorial, a cautionary and 
an editorial and cautionary accidental."""

score = Score('cautionary accidentals')
p = score.add_part('cautionary')
raise NotImplementedError()