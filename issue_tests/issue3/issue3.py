import os

from quicktions import Fraction

from musicscore.basic_functions import flatten
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])
durations = [Fraction(2, 3), Fraction(279, 784), Fraction(899, 2352), Fraction(25, 42)]

durations = flatten(durations)


def get_chords():
    return score.get_measure(1).get_part(1).voices[1].chords


sf = SimpleFormat(quarter_durations=durations)
score = TreeScoreTimewise()
sf.to_stream_voice().add_to_score(score)
print('after add_to_score')
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))
score.update_measures()
print('after update_measures')
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))
score.fill_with_rest()
print('after fill_with_rest')
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))
score.preliminary_adjoin_rests()
print('after preliminary_adjoin_rests')
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))
score.add_beats()
print('after add_beats')
print([sum([chord.quarter_duration for chord in beat.chords]) for beat in score.get_beats()])
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))
score.quantize()
print('after quantize')
print([chord.quarter_duration for chord in get_chords()])
print(float(sum([chord.quarter_duration for chord in get_chords()])))

xml_path = path + '_1.xml'
score.write(xml_path)
