from unittest import TestCase

from musicscore.musicstream.jsoninterface import ChordDict, AttributeIsNeededError


class TestChordDict(TestCase):
    def test_midis_needed_error(self):
        with self.assertRaises(AttributeIsNeededError):
            ChordDict(
                {
                    'quarter_duration': 10
                }
            )

    def test_quarter_duration_needed_error(self):
        with self.assertRaises(AttributeIsNeededError):
            ChordDict(
                {
                    'midis': 70
                }
            )

    def test_export_chord(self):
        chd = ChordDict(
            {
                'quarter_duration': 10,
                'midis': 60
            }
        )

        ch = chd.get_chord()
        expected = chd.chord_dict['quarter_duration'], chd.chord_dict['midis']
        actual = ch.quarter_duration, ch.midis[0].value
        self.assertEqual(expected, actual)
