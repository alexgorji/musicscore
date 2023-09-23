from musicscore import QuarterDuration, Part, Chord
from musicscore.exceptions import MetronomeWrongBeatUnitError
from musicscore.metronome import Metronome
from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLSound


class TestCase(IdTestCase):
    def test_metronome_init(self):
        m = Metronome(100)
        assert isinstance(m.beat_unit, QuarterDuration)
        assert m.per_minute == 100
        assert m.xml_per_minute.value_ == '100'
        assert m.beat_unit == 1
        assert m.xml_beat_unit.value_ == 'quarter'
        assert len(m.get_xml_beat_dot_objects()) == 0

    def test_metronome_dotted(self):
        m = Metronome(100, beat_unit=1.5)
        assert m.xml_beat_unit.value_ == 'quarter'
        assert len(m.get_xml_beat_dot_objects()) == 1

        m = Metronome(100, beat_unit=2 + 1 + 0.5)
        assert m.xml_beat_unit.value_ == 'half'
        assert len(m.get_xml_beat_dot_objects()) == 2

    def test_metronome_change_values(self):
        m = Metronome(100)
        assert m.xml_beat_unit.value_ == 'quarter'
        assert len(m.get_xml_beat_dot_objects()) == 0
        m.beat_unit = 3
        assert m.xml_beat_unit.value_ == 'half'
        assert len(m.get_xml_beat_dot_objects()) == 1

    def test_metronome_wrong_beat_units(self):
        with self.assertRaises(MetronomeWrongBeatUnitError):
            Metronome(100, 1.1)
        with self.assertRaises(MetronomeWrongBeatUnitError):
            Metronome(100, 2 / 3)
        with self.assertRaises(MetronomeWrongBeatUnitError):
            Metronome(100, 6 / 5)

    def test_metronome_sound(self):
        m = Metronome(100)
        assert isinstance(m.sound, XMLSound)
        assert m.sound.tempo == 100
        m = Metronome(100, beat_unit=1.5)
        assert m.sound.tempo == 150

    def test_add_metronome_to_measure(self):
        p = Part('p1')
        ch = Chord(60, 4)
        p.add_chord(ch)
        ch.metronome = Metronome(100, 1.5)
        expected = """<direction placement="above">
      <direction-type>
        <metronome>
          <beat-unit>quarter</beat-unit>
          <beat-unit-dot />
          <per-minute>100</per-minute>
        </metronome>
      </direction-type>
      <sound tempo="150" />
    </direction>
"""
        p.finalize()
        assert p.get_measure(1).xml_direction.to_string() == expected


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
