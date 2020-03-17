import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treechord import TreeChord
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])

score = TreeScoreTimewise()
simple_format = SimpleFormat(quarter_durations=[1, 4])
simple_format.chords[-1].add_grace_chords(TreeChord(midis=[66]), mode='post')
simple_format.to_stream_voice().add_to_score(score)

xml_path = path + '.xml'
score.write(xml_path)
