from musicscore import Score, Chord
from musicscore.lyrics import Lyrics
from musicscore.tests.util import IdTestCase, _generate_xml_lyric
from musicscore.util import _generate_lyrics
from musicxml import XMLLyric, XMLText, XMLElision, XMLSyllabic
from musicxml.exceptions import XMLElementChildrenRequired

test_lyrics_string = ['Bla!', 'Hello World!', 'Clou-dy day.', 'Tra-la-la Ja! Tra-ra! Bah!',
                      'No-body is per-fect! - - Are they?', 'No- - - -body is per- - fect! - - Are they?']


def chord_lyric_assertions(chords, expected, number=1):
    for xl1, ch in zip(expected, chords):
        if xl1:
            xl2 = ch._xml_lyrics[number - 1]
            try:
                assert xl1.to_string() == xl2.to_string()
            except XMLElementChildrenRequired:
                xl1.xsd_check = False
                assert xl1.to_string() == xl2.to_string()
        else:
            assert not ch._xml_lyrics


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

    def test_generate_lyrics_two_syllabic_without_None(self):
        word = [('Syl', 'lable')]
        expected = [
            _generate_xml_lyric(text='Syl', syllabic='begin'),
            _generate_xml_lyric(text='lable', syllabic='end'),
        ]

        xml_lyrics = _generate_lyrics(word)
        for xl1, xl2 in zip(expected, xml_lyrics):
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

    def test_generate_lyrics_single_syllabic_with_None_at_the_end(self):
        word = ('ja!', None)

        expected = [
            _generate_xml_lyric(text='ja!', syllabic='single', extend='start'),
            _generate_xml_lyric(extend='stop'),
        ]

        xml_lyrics = _generate_lyrics(word)

        for xl1, xl2 in zip(expected, xml_lyrics):
            try:
                assert xl1.to_string() == xl2.to_string()
            except XMLElementChildrenRequired:
                xl1.xsd_check = False
                assert xl1.to_string() == xl2.to_string()

    def test_generate_lyrics_syllabic_with_multiple_None_at_the_end(self):
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

        chord_lyric_assertions(chords, expected)

    def test_generate_lyrics_list_syllabic_multiple(self):
        lyrics_1 = [('syl', 'labic')]
        lyrics_2 = [('SYL', 'LABIC')]
        expected_1 = [
            _generate_xml_lyric(text='syl', syllabic='begin'),
            _generate_xml_lyric(text='labic', syllabic='end'),
        ]
        expected_2 = [
            _generate_xml_lyric(text='SYL', syllabic='begin', number=2),
            _generate_xml_lyric(text='LABIC', syllabic='end', number=2),
        ]
        chords = [Chord(60, 1) for _ in range(2)]
        Lyrics(lyrics_1).add_to_chords(chords)
        Lyrics(lyrics_2, number=2).add_to_chords(chords)
        chord_lyric_assertions(chords, expected_1)
        chord_lyric_assertions(chords, expected_2, 2)

    def test_generate_lyrics_list_syllabic_multiple_show_number(self):
        lyrics_1 = [('syl', 'labic')]
        lyrics_2 = [('SYL', 'LABIC')]
        first_syllable_1 = XMLLyric(number='1')
        first_syllable_1.add_child(XMLSyllabic('single'))
        first_syllable_1.add_child(XMLText('1.'))
        first_syllable_1.add_child(XMLElision(' '))
        first_syllable_1.add_child(XMLSyllabic('begin'))
        first_syllable_1.add_child(XMLText('syl'))

        first_syllable_2 = XMLLyric(number='2')
        first_syllable_2.add_child(XMLSyllabic('single'))
        first_syllable_2.add_child(XMLText('2.'))
        first_syllable_2.add_child(XMLElision(' '))
        first_syllable_2.add_child(XMLSyllabic('begin'))
        first_syllable_2.add_child(XMLText('SYL'))

        expected_1 = [
            first_syllable_1,
            _generate_xml_lyric(text='labic', syllabic='end'),
        ]
        expected_2 = [
            first_syllable_2,
            _generate_xml_lyric(text='LABIC', syllabic='end', number=2),
        ]
        chords = [Chord(60, 1) for _ in range(2)]
        Lyrics(lyrics_1, show_number=True).add_to_chords(chords)
        Lyrics(lyrics_2, number=2, show_number=True).add_to_chords(chords)
        chord_lyric_assertions(chords, expected_1)
        chord_lyric_assertions(chords, expected_2, 2)

    def test_generate_lyrics_list_with_None(self):
        chords = [Chord(60, 1) for _ in range(8)]
        Lyrics(['There', 'are', 'two', 'pauses!', None, None, 'And', 'go!']).add_to_chords(chords)
        assert chords[4].xml_lyrics == []
        assert chords[5].xml_lyrics == []

    def test_generate_lyrics_with_kwargs(self):
        words = [('No', None, None, 'body'), 'is', ('per', None, None, 'fect!', None, None), 'Are', 'they?']
        expected = [
            _generate_xml_lyric(text='No', syllabic='begin', default_y=-10),
            None,
            None,
            _generate_xml_lyric(text='body', syllabic='end', default_y=-10),
            _generate_xml_lyric(text='is', syllabic='single', default_y=-10),
            _generate_xml_lyric(text='per', syllabic='begin', default_y=-10),
            None,
            None,
            _generate_xml_lyric(text='fect!', syllabic='end', extend='start', default_y=-10),
            _generate_xml_lyric(extend='continue', default_y=-10),
            _generate_xml_lyric(extend='stop', default_y=-10),

            _generate_xml_lyric(text='Are', syllabic='single', default_y=-10),
            _generate_xml_lyric(text='they?', syllabic='single', default_y=-10),
        ]

        chords = [Chord(60, 1) for _ in range(len(expected))]
        Lyrics(words, default_y=-10).add_to_chords(chords)
        chord_lyric_assertions(chords, expected)
