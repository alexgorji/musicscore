from pathlib import Path

from musicscore import Score, Chord
from musicscore.tests.util import IdTestCase
from musicscore.util import XML_DIRECTION_TYPE_CLASSES
from musicxml.xmlelement.xmlelement import XMLSymbol, XMLDynamics, XMLWedge, XMLDashes, XMLBracket, XMLPedal, \
    XMLMetronome, XMLBeatUnit, XMLPerMinute, XMLOctaveShift, XMLHarpPedals, XMLPedalTuning, XMLPedalStep, XMLPedalAlter, \
    XMLStringMute, XMLScordatura, XMLAccord, XMLTuningOctave, XMLTuningStep, XMLImage, XMLPrincipalVoice, XMLPercussion, \
    XMLWood, XMLStaffDivide


class TestDynamics(IdTestCase):
    def test_direction_types(self):
        score = Score(title='Directions')
        p = score.add_part('part-1')
        for dt_class in [cl for cl in XML_DIRECTION_TYPE_CLASSES if cl != XMLDynamics]:
            if dt_class == XMLSymbol:
                dt_obj = dt_class('0')
            elif dt_class == XMLWedge:
                dt_obj = dt_class(type='crescendo')
            elif dt_class == XMLDashes:
                dt_obj = dt_class(type='start')
            elif dt_class == XMLBracket:
                dt_obj = dt_class(type='start', line_end='none')
            elif dt_class == XMLPedal:
                dt_obj = dt_class(type='start')
            elif dt_class == XMLMetronome:
                dt_obj = dt_class()
                dt_obj.add_child(XMLBeatUnit('quarter'))
                dt_obj.add_child(XMLPerMinute('120'))
            elif dt_class == XMLOctaveShift:
                dt_obj = dt_class(type='up')
            elif dt_class == XMLHarpPedals:
                dt_obj = dt_class()
                pt = dt_obj.add_child(XMLPedalTuning())
                pt.add_child(XMLPedalStep('A'))
                pt.add_child(XMLPedalAlter(1))
            elif dt_class == XMLStringMute:
                dt_obj = dt_class(type='on')
            elif dt_class == XMLScordatura:
                dt_obj = dt_class()
                acc = dt_obj.add_child(XMLAccord())
                acc.add_child(XMLTuningStep('A'))
                acc.add_child(XMLTuningOctave(0))
            elif dt_class == XMLImage:
                # dt_obj = dt_class(source='www.example.com')
                continue
            elif dt_class == XMLPrincipalVoice:
                dt_obj = dt_class(type='start', symbol='none')
            elif dt_class == XMLPercussion:
                dt_obj = dt_class()
                dt_obj.add_child(XMLWood('cabasa'))
            elif dt_class == XMLStaffDivide:
                dt_obj = dt_class(type='up')
            else:
                dt_obj = dt_class()

            chord = Chord(midis=60, quarter_duration=4)
            chord.add_direction_type(dt_obj)
            p.add_chord(chord)
        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
