from musicscore.chord import Chord
from musicscore.dynamics import DYNAMICS, Dynamics
from musicxml.xmlelement.xmlelement import XMLPp, XMLFf, XMLSfpp, XMLP, XMLF

from musicscore.tests.util import ChordTestCase


class TestDynamics(ChordTestCase):
    def test_dynamics_init(self):
        d = Dynamics('pp')
        assert d.xml_object.__class__ == XMLPp

        d = Dynamics('sfpp')
        assert d.xml_object.__class__ == XMLSfpp

    def test_add_dynamics_to_a_chord_consequently(self):
        ch = Chord(60, 1)
        d1 = ch.add_dynamics('p')[0]
        d2 = ch.add_dynamics('f')[0]
        assert ch.xml_direction_types['below'] == [('dynamics', [d1]), ('dynamics', [d2])]
        ch._parent = self.mock_beat
        ch.finalize()
        assert len(ch._xml_directions) == 2
        assert isinstance(ch._xml_directions[0].xml_direction_type.xml_dynamics.get_children()[0], XMLP)
        assert isinstance(ch._xml_directions[1].xml_direction_type.xml_dynamics.get_children()[0], XMLF)

    def test_add_dynamics(self):
        for dynamics in DYNAMICS:
            ch = Chord(60, 1)
            ch._parent = self.mock_beat
            ch.add_dynamics(dynamics)
            ch.finalize()
            assert len(ch._xml_directions) == 1
            d = ch._xml_directions[0]
            assert d.placement == 'below'
            assert d.xml_direction_type.xml_dynamics.get_children()[0].__class__ == DYNAMICS[dynamics]

    def test_add_dynamics_placement(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics('pp', placement='above')
        ch.finalize()
        d = ch._xml_directions[0]
        assert d.placement == 'above'

    def test_add_multiple_dynamics(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics(['pp', 'ff'], 'below')
        ch.finalize()
        d = ch._xml_directions[0]
        dts = d.find_children('XMLDirectionType')
        assert d.placement == 'below'
        assert dts[0].xml_dynamics.get_children()[0].__class__ == XMLPp
        assert dts[1].xml_dynamics.get_children()[0].__class__ == XMLFf

        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics('pp', 'above')
        ch.add_dynamics('ff', 'below')
        ch.finalize()
        ds = ch._xml_directions
        assert [ds[0].placement, ds[1].placement] == ['above', 'below']
        assert ds[0].xml_direction_type.xml_dynamics.get_children()[0].__class__ == XMLPp
        assert ds[1].xml_direction_type.xml_dynamics.get_children()[0].__class__ == XMLFf
