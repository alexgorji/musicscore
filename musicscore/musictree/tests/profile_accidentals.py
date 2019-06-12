# import cProfile
# import os
#
# from musicscore.musictree.treechord import TreeChord
# from musicscore.musictree.treescoretimewise import TreeScoreTimewise
#
# path = os.path.abspath(__file__).split('.')[0]
#
#
# def p():
#     score = TreeScoreTimewise()
#     score.add_measure()
#     score.add_part('one')
#     midis = [60, 61, 62, 60, 63, 64, 65, 61]
#     for midi in midis:
#         score.add_chord(1, 1, TreeChord(midi, quarter_duration=0.5))
#
#     score.finish()
#     score.write(path=path)
#
#
# cProfile.run('p()', sort="tottime")
