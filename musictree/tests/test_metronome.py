from musictree import QuarterDuration
from musictree.exceptions import MetronomeWrongBeatUnitException
from musictree.metronome import Metronome
from musictree.tests.util import IdTestCase


class TestCase(IdTestCase):
    def test_metronome_init(self):
        m = Metronome(100)
        assert isinstance(m.beat_unit, QuarterDuration)
        assert m.per_minute == 100
        assert m.xml_per_minute.value_ == '100'
        assert m.beat_unit == 1
        assert m.xml_beat_unit.value_ == 'quarter'
        assert m.get_xml_beat_dot_objects() is []
        assert m.sound.tempo == 100

    def test_metronome_dotted(self):
        m = Metronome(100, beat_unit=1.5)
        assert m.xml_beat_unit.value_ == 'quarter'
        assert len(m.get_xml_beat_dot_objects()) == 1

    def test_metronome_change_values(self):
        m = Metronome(100)
        assert m.xml_beat_unit.value_ == 'quarter'
        assert len(m.get_xml_beat_dot_objects()) == 0
        m.beat_unit = 3
        assert m.xml_beat_unit.value_ == 'halb'
        assert len(m.get_xml_beat_dot_objects()) == 1

    def test_metronome_wrong_beat_units(self):
        with self.assertRaises(MetronomeWrongBeatUnitException):
            Metronome(100, 1.2)
        with self.assertRaises(MetronomeWrongBeatUnitException):
            Metronome(100, 2 / 3)


"""
direction placement="above">
        <direction-type>
          <metronome default-y="40" font-family="Finale Maestro" font-size="12" halign="left" relative-y="30">
            <beat-unit>quarter</beat-unit>
            <beat-unit-dot/>
            <per-minute font-family="Times New Roman" font-size="12">100</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="150"/>
      </direction>
"""

"""
      <direction placement="above">
        <direction-type>
          <words font-size="12" font-weight="normal" relative-y="30">Andante </words>
        </direction-type>
        <direction-type>
          <metronome font-family="EngraverTextT" font-size="12" parentheses="yes" relative-y="30" relative-x="90">
            <beat-unit>quarter</beat-unit>
            <per-minute font-family="Times New Roman" font-size="12">80</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="80"/>
      </direction>
"""

"""
      <direction placement="above">
        <direction-type>
          <metronome font-family="Finale Maestro" font-size="12" parentheses="yes" relative-y="30">
            <beat-unit>quarter</beat-unit>
            <beat-unit-dot/>
            <beat-unit>quarter</beat-unit>
          </metronome>
        </direction-type>
      </direction>
"""

"""
      <direction placement="above">
        <direction-type>
          <metronome font-family="Finale Maestro" font-size="12" parentheses="yes" relative-y="30">
            <beat-unit>quarter</beat-unit>
            <per-minute font-family="Times New Roman" font-size="12">120</per-minute>
          </metronome>
        </direction-type>
        <sound tempo="120"/>
      </direction>
"""

"""
      <direction placement="above">
        <direction-type>
          <metronome font-family="Finale Maestro" font-size="12" relative-y="30">
            <beat-unit>quarter</beat-unit>
            <beat-unit>half</beat-unit>
          </metronome>
        </direction-type>
      </direction>
"""
