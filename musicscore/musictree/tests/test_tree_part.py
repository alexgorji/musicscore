from unittest import TestCase

from musicscore.musictree.treebeat import TreeBeat
from musicscore.musictree.treemeasure import TreeMeasure
from musicscore.musictree.treepart import TreePart

class Test(TestCase):

    def test_beats(self):
        m = TreeMeasure(time=(3, 8, 2, 4))
        p = TreePart(id='one')
        m.add_child(p)
        p.set_beats()
        result = [0.5, 0.5, 0.5, 1.0, 1.0]
        self.assertEqual([beat.duration for beat in p.get_beats()], result)
        result = [0, 0.5, 1.0, 1.5, 2.5]
        self.assertEqual([beat.offset for beat in p.get_beats()], result)
        result = [4, 4, 4, 8, 8]
        self.assertEqual([beat.max_division for beat in p.get_beats()], result)
        p.get_beats()[3].max_division = 5
        result = [4, 4, 4, 5, 8]
        self.assertEqual([beat.max_division for beat in p.get_beats()], result)
        with self.assertRaises(ValueError):
            p.set_beats([TreeBeat(duration=0.5), TreeBeat(duration=0.5), TreeBeat(duration=0.5)])
        p.set_beats([TreeBeat(duration=1), TreeBeat(duration=0.5), TreeBeat(duration=2)])
        result = [0, 1, 1.5]
        self.assertEqual([beat.offset for beat in p.get_beats()], result)
