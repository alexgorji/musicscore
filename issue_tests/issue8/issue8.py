import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])
xml_path = path + '.xml'
score = TreeScoreTimewise()
# quarter_durations = [Fraction(918, 515), Fraction(382, 485), Fraction(658, 429), Fraction(577, 449), Fraction(471, 874),
#                      Fraction(998, 963), Fraction(589, 759), Fraction(1096, 669), Fraction(589, 414),
#                      Fraction(589, 594), Fraction(169, 140), Fraction(944, 941), Fraction(1431, 923),
#                      Fraction(658, 555), Fraction(658, 481), Fraction(1105, 784), Fraction(221, 392),
#                      Fraction(221, 196), Fraction(221, 112), Fraction(663, 784), Fraction(663, 392), Fraction(221, 784)]
#
# limit = 11
# quarter_durations = [sum(quarter_durations[:-limit])] + quarter_durations[-limit:]
# print([float(qd) for qd in quarter_durations])
quarter_durations = [0.99999479229065, 1.0031880977683316, 1.5503791982665223, 1.1855855855855857, 1.367983367983368,
                     1.409438775510204, 0.5637755102040817, 1.1275510204081634, 1.9732142857142858, 0.8456632653061225,
                     1.691326530612245, 0.28188775510204084]
# quarter_durations = [4, 0]
# sf = SimpleFormat(durations=quarter_durations, midis=[60, 0])
sf = SimpleFormat(quarter_durations=quarter_durations)
score.set_time_signatures(round(sum(quarter_durations)))
# print([float(chord.quarter_duration) for chord in sf.chords])
sf.to_stream_voice().add_to_score(score)
#
# # score.update_measures()
# # score.fill_with_rest()
# # # score.preliminary_adjoin_rests()
# # # score.add_beats()
# # # score.quantize()
# print(score.get_children_by_type(TreeMeasure))
# print([float(chord.quarter_duration) for chord in score.get_measure(-1).get_part(1).chords])
score.write(xml_path)
TreeChord()
