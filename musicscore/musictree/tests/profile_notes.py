from musicscore.musictree.midi import Midi
from musicscore.musictree.treenote import TreeNote
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
import os
import cProfile

from musicscore.tree.tree import Tree

path = os.path.abspath(__file__).split('.')[0]


def p():
    score = TreeScoreTimewise()
    score.add_part('one')

    midis = [60]*500

    for index, midi in enumerate(midis):
        if index % 8 == 0:
            score.add_measure()
        score.add_note((index//8 + 1), 1, TreeNote(event=Midi(midi).get_pitch_rest(), quarter_duration=0.5))

    score.finish()
    score.write(path=path)


cProfile.run('p()', sort="tottime")
