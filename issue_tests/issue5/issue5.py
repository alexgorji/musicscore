import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])
score = TreeScoreTimewise()

sf = SimpleFormat(durations=[4])
sf.chords[0].add_dynamics('ff')
sf.to_stream_voice().add_to_score(score, part_number=1)
# sf.chords[0].remove_dynamics()
sf.to_stream_voice().add_to_score(score, part_number=2)
# sf.chords[0].add_dynamics('p')
sf.to_stream_voice().add_to_score(score, part_number=3)
xml_path = path + '_1.xml'
score.write(xml_path)
