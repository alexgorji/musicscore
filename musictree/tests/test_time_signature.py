from unittest import TestCase

from musictree.treetimesignature import TreeTimeSignature


class TestTreeTimeSignature(TestCase):
    def test_time_signature_default(self):
        t = TreeTimeSignature()
        assert t.beat == 4
        assert t.beat_type == 4

    def test_check_values(self):
        with self.assertRaises(TypeError):
            TreeTimeSignature(None, 4)
        with self.assertRaises(TypeError):
            TreeTimeSignature(4, None)
        with self.assertRaises(TypeError):
            TreeTimeSignature(4.2, 4)
        with self.assertRaises(TypeError):
            TreeTimeSignature(4, 4.2)
        with self.assertRaises(TypeError):
            TreeTimeSignature('4', 4)
        with self.assertRaises(TypeError):
            TreeTimeSignature(4, '4')
        for beat_type in [3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21]:
            with self.assertRaises(ValueError):
                TreeTimeSignature(3, beat_type)
