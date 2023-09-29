from musicscore.exceptions import LyricsWrongNumberOfChordsError
from musicscore.util import _generate_lyrics


class Lyrics:
    def __init__(self, word_groups, number=1, show_number=False, **kwargs):
        self._word_groups = word_groups
        self._number = number
        self._show_number = show_number
        self._xml_lyrics = _generate_lyrics(word_groups, number=number, show_number=show_number, **kwargs)

    @property
    def number(self):
        return self._number

    @property
    def show_number(self):
        return self._show_number

    @property
    def word_groups(self):
        return self._word_groups

    @property
    def xml_lyrics(self):
        return self._xml_lyrics

    def add_to_chords(self, chords):
        if len(chords) != len(self.xml_lyrics):
            raise LyricsWrongNumberOfChordsError(
                f'number of chords: {len(chords)}, number of xml_lyrics: {len(self.xml_lyrics)}')

        for ch, xl in zip(chords, self.xml_lyrics):
            if xl:
                ch.add_lyric(xl)
