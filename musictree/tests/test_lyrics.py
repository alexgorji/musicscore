from musictree import Score, Chord
from musictree.lyrics import Lyrics
from musictree.tests.util import IdTestCase, _generate_xml_lyric
from musictree.util import _generate_lyrics
from musicxml import XMLLyric
from musicxml.exceptions import XMLElementChildrenRequired

test_lyrics_string = ['Bla!', 'Hello World!', 'Clou-dy day.', 'Tra-la-la Ja! Tra-ra! Bah!',
                      'No-body is per-fect! - - Are they?', 'No- - - -body is per- - fect! - - Are they?']


class TestLyrics(IdTestCase):

    def setUp(self):
        super().setUp()
        self.score = Score()
        self.part = self.score.add_part('p1')

    def test_generate_lyrics_one_word(self):
        xml_lyrics = _generate_lyrics('Bla!')
        expected = _generate_xml_lyric(text='Bla!', syllabic='single')
        assert xml_lyrics[0].to_string() == expected.to_string()

        xml_lyrics = _generate_lyrics(['Bla!'])
        expected = _generate_xml_lyric(text='Bla!', syllabic='single')
        assert xml_lyrics[0].to_string() == expected.to_string()

    def test_generate_lyrics_list_words(self):
        words = ['Hello', 'World!']
        xml_lyrics = _generate_lyrics(words)
        expected = [_generate_xml_lyric(text=t, syllabic='single') for t in words]

        for xl1, xl2 in zip(xml_lyrics, expected):
            assert xl1.to_string() == xl2.to_string()

    def test_generate_lyrics_syllabic_without_None(self):
        word = [('Clou', 'di', 'ness')]
        expected = [
            _generate_xml_lyric(text='Clou', syllabic='begin'),
            _generate_xml_lyric(text='di', syllabic='middle'),
            _generate_xml_lyric(text='ness', syllabic='end'),
        ]

        xml_lyrics = _generate_lyrics(word)
        for xl1, xl2 in zip(expected, xml_lyrics):
            assert xl1.to_string() == xl2.to_string()

        word = ('Clou', 'di', 'ness')
        xml_lyrics = _generate_lyrics(word)

        for xl1, xl2 in zip(expected, xml_lyrics):
            assert xl1.to_string() == xl2.to_string()

    def test_generate_lyrics_list_syllabic_without_None(self):
        words = [('Tra', 'la', 'la'), 'Ja!', ('Tra', 'ra!'), 'Bah']

        expected = [
            _generate_xml_lyric(text='Tra', syllabic='begin'),
            _generate_xml_lyric(text='la', syllabic='middle'),
            _generate_xml_lyric(text='la', syllabic='end'),
            _generate_xml_lyric(text='Ja!', syllabic='single'),
            _generate_xml_lyric(text='Tra', syllabic='begin'),
            _generate_xml_lyric(text='ra!', syllabic='end'),
            _generate_xml_lyric(text='Bah', syllabic='single'),
        ]

        xml_lyrics = _generate_lyrics(words)

        for xl1, xl2 in zip(expected, xml_lyrics):
            assert xl1.to_string() == xl2.to_string()

    def test_generate_lyrics_syllabic_with_None_in_between(self):
        word = ('per', None, None, 'fect!')

        expected = [
            _generate_xml_lyric(text='per', syllabic='begin'),
            None,
            None,
            _generate_xml_lyric(text='fect!', syllabic='end'),
        ]

        xml_lyrics = _generate_lyrics(word)

        for xl1, xl2 in zip(expected, xml_lyrics):
            if xl1:
                assert xl1.to_string() == xl2.to_string()
            else:
                assert xl1 == xl2 is None

    def test_generate_lyrics_syllabic_with_None_at_the_end(self):
        word = ('per', 'fect!', None, None)

        expected = [
            _generate_xml_lyric(text='per', syllabic='begin'),
            _generate_xml_lyric(text='fect!', syllabic='end', extend='start'),
            _generate_xml_lyric(extend='continue'),
            _generate_xml_lyric(extend='stop'),
        ]

        xml_lyrics = _generate_lyrics(word)

        for xl1, xl2 in zip(expected, xml_lyrics):
            try:
                assert xl1.to_string() == xl2.to_string()
            except XMLElementChildrenRequired:
                xl1.xsd_check = False
                assert xl1.to_string() == xl2.to_string()

    def test_generate_lyrics_list_syllabic_with_None_in_between_and_at_the_end(self):
        words = [('No', None, None, 'body'), 'is', ('per', None, None, 'fect!', None, None), 'Are', 'they?']
        expected = [
            _generate_xml_lyric(text='No', syllabic='begin'),
            None,
            None,
            _generate_xml_lyric(text='body', syllabic='end'),
            _generate_xml_lyric(text='is', syllabic='single'),
            _generate_xml_lyric(text='per', syllabic='begin'),
            None,
            None,
            _generate_xml_lyric(text='fect!', syllabic='end', extend='start'),
            _generate_xml_lyric(extend='continue'),
            _generate_xml_lyric(extend='stop'),

            _generate_xml_lyric(text='Are', syllabic='single'),
            _generate_xml_lyric(text='they?', syllabic='single'),
        ]

        xml_lyrics = _generate_lyrics(words)

        for xl1, xl2 in zip(expected, xml_lyrics):
            if xl1:
                try:
                    assert xl1.to_string() == xl2.to_string()
                except XMLElementChildrenRequired:
                    xl1.xsd_check = False
                    assert xl1.to_string() == xl2.to_string()
            else:
                assert xl1 == xl2 is None

    def test_generate_lyrics_list_syllabic_with_None_in_between_and_at_the_end_add_to_chords(self):
        words = [('No', None, None, 'body'), 'is', ('per', None, None, 'fect!', None, None), 'Are', 'they?']
        expected = [
            _generate_xml_lyric(text='No', syllabic='begin'),
            None,
            None,
            _generate_xml_lyric(text='body', syllabic='end'),
            _generate_xml_lyric(text='is', syllabic='single'),
            _generate_xml_lyric(text='per', syllabic='begin'),
            None,
            None,
            _generate_xml_lyric(text='fect!', syllabic='end', extend='start'),
            _generate_xml_lyric(extend='continue'),
            _generate_xml_lyric(extend='stop'),

            _generate_xml_lyric(text='Are', syllabic='single'),
            _generate_xml_lyric(text='they?', syllabic='single'),
        ]

        chords = [Chord(60, 1) for _ in range(len(expected))]
        Lyrics(words).add_to_chords(chords)


        for xl1, ch in zip(expected, chords):
            if xl1:
                xl2 = ch._xml_lyrics[0]
                try:
                    assert xl1.to_string() == xl2.to_string()
                except XMLElementChildrenRequired:
                    xl1.xsd_check = False
                    assert xl1.to_string() == xl2.to_string()
            else:
                assert not ch._xml_lyrics
