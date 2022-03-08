from musictree.chord import Chord
from musictree.dynamics import DYNAMICS, Dynamics
from musicxml.xmlelement.xmlelement import XMLPp, XMLFf, XMLSfpp

from musictree.tests.util import ChordTestCase


class TestDynamics(ChordTestCase):
    def test_dynamics_init(self):
        d = Dynamics('pp')
        assert d.xml_object.__class__ == XMLPp

        d = Dynamics('sfpp')
        assert d.xml_object.__class__ == XMLSfpp

    def test_add_dynamics(self):
        for dynamics in DYNAMICS:
            ch = Chord(60, 1)
            ch._parent = self.mock_beat
            ch.add_dynamics(dynamics)
            ch.final_updates()
            assert len(ch._xml_directions) == 1
            d = ch._xml_directions[0]
            assert d.placement == 'below'
            assert d.xml_direction_type.xml_dynamics.get_children()[0].__class__ == DYNAMICS[dynamics]

    def test_add_dynamics_placement(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics('pp', placement='above')
        ch.final_updates()
        d = ch._xml_directions[0]
        assert d.placement == 'above'

    def test_add_multiple_dynamics(self):
        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics(['pp', 'ff'], 'below')
        ch.final_updates()
        d = ch._xml_directions[0]
        dts = d.find_children('XMLDirectionType')
        assert d.placement == 'below'
        assert dts[0].xml_dynamics.get_children()[0].__class__ == XMLPp
        assert dts[1].xml_dynamics.get_children()[0].__class__ == XMLFf

        ch = Chord(60, 1)
        ch._parent = self.mock_beat
        ch.add_dynamics('pp', 'above')
        ch.add_dynamics('ff', 'below')
        ch.final_updates()
        ds = ch._xml_directions
        assert [ds[0].placement, ds[1].placement] == ['above', 'below']
        assert ds[0].xml_direction_type.xml_dynamics.get_children()[0].__class__ == XMLPp
        assert ds[1].xml_direction_type.xml_dynamics.get_children()[0].__class__ == XMLFf

    def test_add_dynamics_after_creating_notes(self):
        pass