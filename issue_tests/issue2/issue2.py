import os

from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescoretimewise import TreeScoreTimewise

path = str(os.path.abspath(__file__).split('.')[0])

score = TreeScoreTimewise()
score.page_style.orientation = 'landscape'
score.add_title('BIG IMPORTANT TITLE')
score.add_subtitle('unimportant subtitle')
score.add_composer('me')
score.add_text('some text')

simple_format = SimpleFormat(quarter_durations=4)
simple_format.to_stream_voice().add_to_score(score=score)

score.page_style.orientation = 'portrait'
# conversion of default_x and default_y in CreditWords (child of Credit)
xml_path = path + '_1.xml'
score.write(xml_path)
