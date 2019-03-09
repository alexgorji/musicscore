from unittest import TestCase
from musicscore.dtd.music_data import MusicData, Direction, Backup
from musicscore.dtd.note import Note, Duration
from musicscore.dtd.dtd import ChildOccurrenceDTDConflict, ChildTypeDTDConflict, ChildIsNotOptional


class TestMusicData(TestCase):
    def setUp(self):
        self.music_data = MusicData()

    def test_add_child_type(self):
        self.music_data.add_child(Direction())
        self.music_data.add_child(Note())
        with self.assertRaises(ChildTypeDTDConflict):
            self.music_data.add_child(Duration())

    def test_add_child_max_occurrence(self):
        # self.music_data.reset_children()
        self.music_data.add_child(Direction())
        self.music_data.add_child(Direction())
        self.music_data.add_child(Note())
        self.music_data.add_child(Backup())

    #
    # def test_close(self):
    #     self.note.reset_children()
    #     self.note.add_child(FullNote())
    #     self.note.add_child(Grace())
    #     self.note.close()
    #     result = ['Grace', 'FullNote', 'Instrument', 'EditorialVoice', 'Type', 'Dot', 'Accidental', 'TimeModification',
    #               'Stem', 'Notehead', 'NotheadText', 'Staff', 'Beam', 'Notations', 'Lyric', 'Play']
    #     self.assertEqual([node.type_.__name__ for node in self.note._DTD.get_current_combination()], result)
    #
    #     self.note.reset_children()
    #     self.note.add_child(FullNote())
    #     with self.assertRaises(ChildIsNotOptional):
    #         self.note.close()
    #
    def test_sort_children(self):
        # self.music_data.reset_children()
        self.music_data.add_child(Direction())
        self.music_data.add_child(Direction())
        self.music_data.add_child(Note())
        self.music_data.add_child(Backup())
        # result = ['FullNote', 'Duration', 'Tie', 'Tie', 'Beam', 'Beam']
        # self.assertEqual([type(child).__name__ for child in self.note.get_children()], result)
        # self.music_data.sort_children()
