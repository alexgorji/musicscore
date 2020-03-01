import os

from quicktions import Fraction

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treeclef import ALTO_CLEF, TREBLE_CLEF
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])
durations = [Fraction(31, 14), Fraction(93, 56), Fraction(31, 28), Fraction(155, 56), Fraction(57, 56)]
clefs = [ALTO_CLEF, None, None, TREBLE_CLEF, ALTO_CLEF]


def get_chords():
    return score.get_measure(1).get_part(1).voices[1].chords


sf = SimpleFormat(quarter_durations=durations)
for chord, clef in zip(sf.chords, clefs):
    if clef:
        chord.add_clef(clef)

score = TreeScoreTimewise()
score.max_division = 7
sf.to_stream_voice().add_to_score(score)
xml_path = path + '_1.xml'
score.write(xml_path)
