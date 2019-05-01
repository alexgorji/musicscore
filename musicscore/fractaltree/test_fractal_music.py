import os
from unittest import TestCase

from musicscore import basic_functions
from musicscore.fractaltree.fractaltree import FractalMusic
from musicscore.musicstream.streamvoice import SimpleFormat
from musicscore.musictree.treescore_timewise import TreeScoreTimewise
from musicscore.musicxml.score_templates.xml_test_score import TestScore

path = os.path.abspath(__file__).split('.')[0]


class Test(TestCase):

    def test_1(self):
        fm = FractalMusic(duration=12, tree_permutation_order=(3, 1, 2), proportions=[1, 2, 3], multi=(1, 2))
        fm.midi_generator.midi_range = [55, 72]
        fm.add_layer()
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)
        fm.add_layer(lambda n: True if n.fractal_order > 1 else False)

        score = TreeScoreTimewise()
        for index, layer in enumerate(fm.layers):
            sf = SimpleFormat()
            for node in basic_functions.flatten(layer):
                sf.add_chord(node.chord.__deepcopy__())
            v = sf.to_voice(1)
            v.add_to_score(score, 1, index + 1)

        result_path = path + '_test_1'
        score.write(path=result_path)
        TestScore().assert_template(result_path=result_path)
