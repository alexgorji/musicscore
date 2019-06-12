# from musicscore.musictree.treechord import TreeChord
# from musicscore.musictree.treescoretimewise import TreeScoreTimewise
# import os
# import cProfile
#
# path = os.path.abspath(__file__).split('.')[0]
#
#
# def p():
#     score = TreeScoreTimewise()
#     score.add_part('one')
#
#     # midis = [(60, 61)]*500
#     midis = [60]*500
#
#     for index, midi in enumerate(midis):
#         if index % 8 == 0:
#             score.add_measure()
#         score.add_chord((index//8 + 1), 1, TreeChord(midi, quarter_duration=0.5))
#
#     score.finish()
#     score.write(path=path)
#
#
# cProfile.run('p()', sort="tottime")
