"""
All <direction> elements defined in MusicXML.
"""
from pathlib import Path

from musicscore.tests.util import IdTestCase
from musicxml.xmlelement.xmlelement import XMLRehearsal, XMLDynamics, XMLOtherDynamics, XMLSegno, XMLCoda, XMLWords, \
    XMLEyeglasses, XMLDashes, XMLBracket, XMLOctaveShift, XMLPedal, XMLMetronome, XMLBeatUnit, XMLPerMinute, \
    XMLHarpPedals, XMLPedalStep, XMLPedalAlter, XMLPedalTuning, XMLDamp, XMLDampAll, XMLScordatura, XMLAccord, \
    XMLTuningStep, XMLTuningOctave, XMLTuningAlter, XMLAccordionRegistration, XMLAccordionHigh, XMLAccordionMiddle, \
    XMLAccordionLow, XMLWedge, XMLPrint, XMLBarline, XMLBarStyle

""""
XML_DIRECTION_TYPE_CLASSES = [
    XMLSymbol, XMLStringMute, XMLImage, XMLPrincipalVoice, XMLPercussion, XMLStaffDivide, XMLOtherDirection
]
"""
from musicscore import Score, Chord


class TestLily31a(IdTestCase):
    def test_lily_31a_Directions(self):

        score = Score(title="MusicXML directions (attached to staff)")
        part = score.add_part('p1')

        for rehearsal, enclosure in zip(['A', 'B', 'Test', 'Crc'], ['square', 'none', 'rectangle', 'circle']):
            r = XMLRehearsal(rehearsal, enclosure=enclosure)
            ch = Chord(60, 1)
            ch.add_direction_type(r)
            part.add_chord(ch)

        for dt in [XMLSegno(), XMLCoda(), XMLWords('words'), XMLEyeglasses()]:
            ch = Chord(60, 1)
            if isinstance(dt, XMLWords):
                ch.add_direction_type(dt, 'below')
            else:
                ch.add_direction_type(dt, 'above')
            part.add_chord(ch)

        dynamics = ['p', 'pp', 'ppp', 'pppp', 'ppppp', 'pppppp', 'f', 'ff', 'fff', 'ffff', 'fffff', 'ffffff', 'mp',
                    'mf',
                    'sf', 'sfp', 'sfpp', 'fp', 'rf', 'rfz', 'sfz', 'sffz', 'fz']
        for d in dynamics:
            ch = Chord(60, 1)
            ch.add_dynamics(d)
            part.add_chord(ch)

        ch = Chord(60, 1)
        d = XMLDynamics()
        d.add_child(XMLOtherDynamics('abc-ffz'))
        ch.add_direction_type(d, placement='below')
        part.add_chord(ch)

        for w in ['crescendo', 'stop']:
            ch = Chord(60, 1)
            ch.add_wedge(w)
            part.add_chord(ch)

        for x in ['start', 'stop']:
            ch = Chord(60, 1)
            ch.add_direction_type(XMLDashes(type=x))
            part.add_chord(ch)

        for x in ['start', 'stop']:
            ch = Chord(60, 1)
            ch.add_direction_type(XMLBracket(type=x, line_end='down'))
            part.add_chord(ch)

        for x in ['down', 'stop']:
            ch = Chord(60, 1)
            ch.add_direction_type(XMLOctaveShift(type=x))
            part.add_chord(ch)

        for x in ['start', ('stop', 'start'), 'continue', 'stop']:
            ch = Chord(60, 1)
            if isinstance(x, tuple):
                ch.add_direction_type(XMLPedal(type=x[0], relative_x=-25, relative_y=-10), 'below')
                ch.add_direction_type(XMLPedal(type=x[1], relative_y=-10), 'below')
            else:
                ch.add_direction_type(XMLPedal(type=x, relative_y=-10), 'below')
            part.add_chord(ch)

        ch = Chord(60, 1)
        m = XMLMetronome()
        m.add_child(XMLBeatUnit('quarter'))
        m.add_child(XMLPerMinute('60'))
        ch.add_direction_type(m)
        part.add_chord(ch)

        ch = Chord(60, 1)
        steps = ['D', 'C', 'B', 'E', 'F', 'G', 'A']
        alters = [0, -1, -1, 0, 0, 1, -1]
        hp = XMLHarpPedals(relative_y=-20, font_size=14)
        for s, a in zip(steps, alters):
            pt = hp.add_child(XMLPedalTuning())
            pt.add_child(XMLPedalStep(s))
            pt.add_child(XMLPedalAlter(a))
        ch.add_direction_type(hp, 'below')
        part.add_chord(ch)

        ch = Chord(60, 1)
        ch.add_direction_type(XMLDamp())
        part.add_chord(ch)

        ch = Chord(60, 1)
        ch.add_direction_type(XMLDampAll())
        part.add_chord(ch)

        """
        <scordatura>
           <accord string="1">
              <tuning-step>E</tuning-step>
              <tuning-octave>5</tuning-octave>
           </accord>
           <accord string="2">
              <tuning-step>A</tuning-step>
              <tuning-octave>4</tuning-octave>
           </accord>
           <accord string="3">
              <tuning-step>E</tuning-step>
              <tuning-alter>-1</tuning-alter>
              <tuning-octave>4</tuning-octave>
           </accord>
           <accord string="4">
              <tuning-step>A</tuning-step>
              <tuning-octave>3</tuning-octave>
           </accord>
        </scordatura>
        """

        sc = XMLScordatura()
        steps = ['E', 'A', 'E', 'A']
        alters = [None, None, -1, None]
        octaves = [5, 4, 4, 3]
        for index, (s, a, o) in enumerate(zip(steps, alters, octaves)):
            st = sc.add_child(XMLAccord(string=index + 1))
            st.add_child(XMLTuningStep(s))
            if a:
                st.add_child(XMLTuningAlter(a))
            st.add_child(XMLTuningOctave(o))

        ch = Chord(60, 1)
        ch.add_direction_type(sc)
        ch.add_lyric('Scordatura')
        part.add_chord(ch)

        """
        <direction>
           <direction-type>
              <accordion-registration>
                 <accordion-high/>
                 <accordion-middle>3</accordion-middle>
              </accordion-registration>
           </direction-type>
        </direction>
        """
        ch = Chord(60, 1)
        ag = XMLAccordionRegistration()
        ag.add_child(XMLAccordionHigh())
        ag.add_child(XMLAccordionMiddle(2))
        ag.add_child(XMLAccordionLow())
        ch.add_direction_type(ag)
        part.add_chord(ch)

        ch = Chord(0, 2)
        part.add_chord(ch)

        ch = Chord(60, 1)
        ch.add_dynamics('p')
        ch.add_direction_type(XMLWords('subito', font_style='italic', relative_y=-20), placement='below')
        part.add_chord(ch)

        ch = Chord(60, 1)
        ch.add_dynamics('ppp')
        ch.add_wedge(XMLWedge(type='crescendo', relative_x=25))
        part.add_chord(ch)

        ch = Chord(60, 1)
        ch.add_dynamics('fff')
        ch.add_wedge(XMLWedge(type='stop', relative_x=-5))
        part.add_chord(ch)

        ch = Chord(0, 1)
        part.add_chord(ch)

        new_systems = [2, 5, 9, 12]
        for m in new_systems:
            part.get_measure(m).xml_object.add_child(XMLPrint(new_system='yes'))

        barline = XMLBarline(location='right')
        barline.add_child(XMLBarStyle('light-light'))
        part.get_measure(13).xml_object.add_child(barline)

        barline = XMLBarline(location='right')
        barline.add_child(XMLBarStyle('light-heavy'))
        part.get_measure(14).xml_object.add_child(barline)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
