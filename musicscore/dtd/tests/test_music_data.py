from unittest import TestCase
from musicscore.musicxml.elements.music_data import MusicData, Direction, Backup
from musicscore.musicxml.elements.note import Note, Duration
from musicscore.dtd.dtd import ChildTypeDTDConflict


# class TestMusicData(TestCase):
#     def setUp(self):
#         self.music_data = MusicData()
#
#     def test_add_child_type(self):
#         self.music_data.add_child(Direction())
#         self.music_data.add_child(Note())
#         with self.assertRaises(ChildTypeDTDConflict):
#             self.music_data.add_child(Duration(1))
#
#     def test_add_child_max_occurrence(self):
#         self.music_data.add_child(Direction())
#         self.music_data.add_child(Direction())
#         self.music_data.add_child(Note())
#         self.music_data.add_child(Backup())
#
#     def test_sort_children(self):
#         self.music_data.add_child(Direction())
#         self.music_data.add_child(Direction())
#         self.music_data.add_child(Note())
#         self.music_data.add_child(Backup())
#         self.music_data.close()
#         result = ['Direction', 'Direction', 'Note', 'Backup']
#         self.assertEqual([type(child).__name__ for child in self.music_data.get_children()], result)


