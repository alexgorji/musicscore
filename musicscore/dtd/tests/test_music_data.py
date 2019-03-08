from unittest import TestCase
from musicscore.dtd.music_data import MusicData, Direction


class TestMusicData(TestCase):
    def setUp(self):
        self.music_data = MusicData()

    def set_add_child(self):
        self.music_data.add_child(Direction)
