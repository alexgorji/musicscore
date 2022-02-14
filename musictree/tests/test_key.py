from unittest import TestCase

from musictree.key import Key


class TestStaff(TestCase):
    def test_key_init(self):
        k = Key()
        assert k.fifths == 0
        k.fifths = 3
        expected = """<key>
  <fifths>3</fifths>
</key>
"""
        assert k.to_string() == expected

    def test_key_copy(self):
        k = Key(fifths=3, show=False)
        copied = k.__copy__()
        assert copied != k
        assert copied.xml_object != k.xml_object
        assert copied.fifths == k.fifths
        assert copied.show == k.show
