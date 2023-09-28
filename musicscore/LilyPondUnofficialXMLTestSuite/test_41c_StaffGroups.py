"""
A huge orchestra score with 28 parts and different kinds of nested bracketed groups. Each part/group is assigned a
name and an abbreviation to be shown before the staff. Also, most of the groups show unbroken barlines,
while the barlines are broken between the groups.
"""
from pathlib import Path

from musicscore import Score, Chord, TrebleClef, BassClef
from musicscore.clef import PercussionClef, AltoClef
from musicscore.tests.util import IdTestCase
from musicxml import XMLTranspose


class TestLily41c(IdTestCase):
    def test_lily_41c_StaffGroups(self):
        score = Score()
        score.page_layout.size = 'A4'
        score.scaling.millimeters = 2.6176
        score.scaling.tenths = 40
        score.page_layout.margins.left = 200
        instruments = {
            'Piccolo': {'abbreviation': 'picc', 'clef': TrebleClef(octave_change=1)},
            'Flute 1': {'abbreviation': 'fl 1'},
            'Flute 2': {'abbreviation': 'fl 2'},
            'Oboe 1': {'abbreviation': 'ob 1'},
            'Oboe 2': {'abbreviation': 'ob 2'},
            'English Horn': {'abbreviation': 'eh', 'transposition': -7},
            'Clarinet in Eb': {'abbreviation': 'cl(Eb)', 'transposition': 3},
            'Clarinet 1 in Bb': {'abbreviation': 'cl(Bb) 1', 'transposition': -2},
            'Clarinet 2 in Bb': {'abbreviation': 'cl(Bb) 2', 'transposition': -2},
            'Bass Clarinet': {'abbreviation': 'bcl', 'clef': BassClef(octave_change=-1), 'transpose': -2},
            'Bassoon 1': {'abbreviation': 'bn 2', 'clef': BassClef()},
            'Bassoon 2': {'abbreviation': 'bn 1', 'clef': BassClef()},
            'Contrabassoon': {'abbreviation': 'cbn', 'clef': BassClef(octave_change=-1)},
            'Horn in F 1': {'abbreviation': 'hn(F) 1', 'transposition': -7},
            'Horn in F 2': {'abbreviation': 'hn(F) 2', 'transposition': -7},
            'Trumpet in C 1': {'abbreviation': 'tp(C) 1'},
            'Trumpet in C 2': {'abbreviation': 'tp(C) 1', },
            'Trombone 1': {'abbreviation': 'tbn', 'clef': BassClef()},
            'Trombone 2': {'abbreviation': 'tbn', 'clef': BassClef()},
            'Tuba': {'abbreviation': 'tb', 'clef': BassClef()},
            'Timpani': {'abbreviation': 'tmp', 'clef': BassClef()},
            'Percussion': {'abbreviation': 'perc', 'clef': PercussionClef()},
            'Harp': {'abbreviation': 'hrp', 'number_of_staves': 2},
            'Piano': {'abbreviation': 'pno', 'number_of_staves': 2},
            'Violin I': {'abbreviation': 'vn 2', },
            'Violin II': {'abbreviation': 'vn 1', },
            'Viola': {'abbreviation': 'va', 'clef': AltoClef()},
            'Cello': {'abbreviation': 'vc', 'clef': BassClef()},
            'Contrabass': {'abbreviation': 'cb', 'clef': BassClef(octave_change=-1)},
        }
        for i, k in enumerate(instruments.keys()):
            part = score.add_part(f'p{i + 1}')
            part.name = k
            part.abbreviation = instruments[k]['abbreviation']

            part.add_chord(Chord(61, 4))
            clef = instruments[k].get('clef')

            if clef:
                part.get_current_measure().get_staff(1).clef = clef
            number_of_staves = instruments[k].get('number_of_staves')
            if number_of_staves == 2:
                part.add_chord(Chord(0, 4), staff_number=2)
            transposition = instruments[k].get('transposition')
            if transposition:
                tr = XMLTranspose()
                tr.xml_chromatic = transposition
                part.get_current_measure().xml_attributes.xml_transpose = tr
            part.add_chord(Chord(0, 4))
            if number_of_staves == 2:
                part.add_chord(Chord(0, 4), staff_number=2)
            part.get_current_measure().new_system = True
        score.group_parts(2, 1, 13, 'bracket')
        score.group_parts(2, 14, 20, 'bracket')
        score.group_parts(2, 25, 29, 'bracket')

        score.group_parts(1, 2, 3, 'square', default_x=-18)
        score.group_parts(1, 4, 5, 'square', default_x=-18)
        score.group_parts(1, 8, 9, 'square', default_x=-18)
        score.group_parts(1, 11, 12, 'square', default_x=-18)
        score.group_parts(1, 14, 15, 'square', default_x=-18)
        score.group_parts(1, 16, 17, 'square', default_x=-18)
        score.group_parts(1, 18, 19, 'square', default_x=-18)
        score.group_parts(1, 25, 26, 'square', default_x=-18)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
