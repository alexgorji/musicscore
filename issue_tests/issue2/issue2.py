import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])

score = TreeScoreTimewise()

simple_format = SimpleFormat(quarter_durations=4)
simple_format.to_stream_voice().add_to_score(score=score)
xml_path = path + '_1.xml'
score.write(xml_path)
