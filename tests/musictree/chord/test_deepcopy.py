from musicscore.musictree.treechord import TreeChord
from musicxmlunittest import XMLTestCase


class Test(XMLTestCase):
    def setUp(self) -> None:
        self.chord = TreeChord()

    def test_1(self):
        self.chord.add_words('1')
        copied = self.chord.__deepcopy__()
        print(copied._current_children[0]._current_children[0].__dict__)