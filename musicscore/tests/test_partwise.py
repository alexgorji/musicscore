from unittest import TestCase
from musicscore.partwise import Partwise


class TestPartwise(TestCase):
    def setUp(self):
        self.partwise = Partwise()

    def test_add_part(self):
        self.partwise.add_part()
        self.partwise.add_part()
        self.partwise.add_part()
        print(self.partwise.to_string())

