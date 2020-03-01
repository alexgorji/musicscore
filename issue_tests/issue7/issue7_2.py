import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise
path = str(os.path.abspath(__file__).split('.')[0])
xml_path = path + '.xml'
score = TreeScoreTimewise()
quarter_durations = [1, 1-0.01, 0.01]
sf = SimpleFormat(quarter_durations=quarter_durations)
score.set_time_signatures(round(sum(quarter_durations)))
sf.to_stream_voice().add_to_score(score)
#
# score.update_measures()
# score.fill_with_rest()
# # score.preliminary_adjoin_rests()
# # score.add_beats()
# # score.quantize()
# print([float(chord.quarter_duration) for chord in score.get_measure(1).get_part(1).chords])
score.write(xml_path)
