from pathlib import Path

from musictree import Score, Chord
from musictree.tests.util import IdTestCase
from musictree.util import XML_DIRECTION_TYPE_CLASSES

dynamics = ['f', 'ff', 'fff', 'ffff', 'fffff', 'ffffff', 'fp', 'fz', 'mf', 'mp', 'p', 'pf', 'pp', 'ppp', 'pppp',
            'ppppp', 'pppppp', 'rf', 'rfz', 'sf', 'sffz', 'sfp', 'sfpp', 'sfz', 'sfzp']


class TestDynamics(IdTestCase):
    def test_dynamics(self):
        score = Score(title='Dynamics')
        p = score.add_part('part-1')
        p.name = ''
        for d in dynamics:
            chord = Chord(midis=60, quarter_duration=4)
            chord.add_dynamics(d)
            p.add_chord(chord)
        wedge_chords = ch1, ch2 = [Chord(midis=60, quarter_duration=4), Chord(midis=60, quarter_duration=4)]
        ch1.add_dynamics('p')
        ch2.add_dynamics('ff')
        ch1.add_wedge('crescendo')
        ch1.add_wedge('stop')

        for chord in wedge_chords:
            p.add_chord(chord)
        xml_path = 'test_9a_dynamics.xml'
        score.export_xml(xml_path)

    def test_direction_types(self):
        score = Score(title='Dynamics')
        p = score.add_part('part-1')
        for dt_class in XML_DIRECTION_TYPE_CLASSES:
            chord = Chord(midis=60, quarter_duration=4)
            chord.add_direction_type(dt_class())
            p.add_chord(chord)
        xml_path = 'test_9b_directions_types.xml'
        score.export_xml(xml_path)
