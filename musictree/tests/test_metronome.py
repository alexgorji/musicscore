from musictree.metronome import Metronome
from musictree.tests.util import IdTestCase


class TestCase(IdTestCase):
    def test_metronome_init(self):
        m = Metronome(100)
        assert m.per_minute == 100
        assert m.xml_per_minute.value_ == '100'
        assert m.beat_unit == 1
        assert m.xml_beat_unit.value_ == 'quarter'
        assert m.xml_beat_dot is None


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
