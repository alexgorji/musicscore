"""
All <notation> elements defined in MusicXML. The lyrics show the notation assigned to each note.
"""
from pathlib import Path

from musicscore import Score, Chord, C, E, G
from musicscore.tests.util import IdTestCase
from musicscore.util import XML_DYNAMIC_CLASSES
from musicxml.xmlelement.xmlelement import XMLFermata, XMLArpeggiate, XMLNonArpeggiate, XMLAccidentalMark, XMLAccent, \
    XMLStrongAccent, XMLStaccato, XMLTenuto, XMLStaccatissimo, XMLSpiccato, XMLScoop, XMLPlop, XMLDoit, XMLFalloff, \
    XMLBreathMark, XMLCaesura, XMLStress, XMLUnstress, XMLTrillMark, XMLTurn, XMLDelayedTurn, XMLInvertedTurn, XMLShake, \
    XMLWavyLine, XMLDetachedLegato, XMLMordent, XMLInvertedMordent, XMLSchleifer, XMLTremolo, XMLUpBow, XMLDownBow, \
    XMLHarmonic, XMLNatural, XMLArtificial, XMLBasePitch, XMLTouchingPitch, XMLSoundingPitch, XMLOpenString, \
    XMLFingering, XMLThumbPosition, XMLPluck, XMLDoubleTongue, XMLTripleTongue, XMLStopped, XMLSnapPizzicato, XMLFret, \
    XMLString, XMLPullOff, XMLHammerOn, XMLBend, XMLBendAlter, XMLWithBar, XMLPreBend, XMLRelease, XMLTap, XMLHeel, \
    XMLToe, XMLFingernails, XMLF, XMLPpp, XMLSfp, XMLOtherDynamics


class TestLily321(IdTestCase):
    def test_lily_321_Notations(self):

        score = Score()
        part = score.add_part('p1')

        xml_notations = [
            XMLFermata(),
            XMLFermata('normal'),
            XMLFermata('angled'),
            XMLFermata('square'),
            XMLFermata(type='inverted'),
            XMLArpeggiate(),
            XMLNonArpeggiate(),
            XMLAccidentalMark('double-sharp'),
            XMLAccent(),
            XMLStrongAccent(),
            XMLStaccato(),
            XMLTenuto(),
            XMLDetachedLegato(),
            XMLStaccatissimo(),
            XMLSpiccato(),
            XMLScoop(),
            XMLPlop(),
            XMLDoit(),
            XMLFalloff(),
            XMLBreathMark(),
            XMLCaesura(),
            XMLStress(),
            XMLUnstress(),
            None,
            XMLTrillMark(),
            XMLTurn(),
            XMLDelayedTurn(),
            XMLInvertedTurn(),
            XMLShake(),
            [XMLWavyLine(type='start'), XMLWavyLine(type='continue'), XMLWavyLine(type='stop')],
            XMLMordent(),
            XMLInvertedMordent(),
            XMLSchleifer(),
            XMLTremolo(3),
            (XMLTurn(), XMLAccidentalMark('natural', placement='below')),
            (XMLTurn(), XMLAccidentalMark('sharp'), XMLAccidentalMark('three-quarters-flat')),
            XMLUpBow(),
            XMLDownBow(),
            XMLHarmonic(),
        ]

        harmonics = [XMLHarmonic() for _ in range(6)]
        harmonics[0].add_child(XMLNatural())
        harmonics[2].add_child(XMLArtificial())
        harmonics[3].add_child(XMLNatural())
        harmonics[3].add_child(XMLBasePitch())
        harmonics[4].add_child(XMLNatural())
        harmonics[4].add_child(XMLTouchingPitch())
        harmonics[5].add_child(XMLNatural())
        harmonics[5].add_child(XMLSoundingPitch())

        xml_notations += harmonics

        xml_notations += [
            XMLOpenString(),
            XMLThumbPosition()
        ]

        fingerings = [XMLFingering() for _ in range(7)]
        fingerings[1].value_ = '1'
        fingerings[2].value_ = '2'
        fingerings[3].value_ = '3'
        fingerings[4].value_ = '4'
        fingerings[5].value_ = '5'
        fingerings[5].value_ = 'something'
        fingerings.append((XMLFingering('2'), XMLFingering('3'), XMLFingering('5')))

        xml_notations += fingerings

        xml_notations += [
            XMLPluck(),
            XMLPluck('a'),
            XMLThumbPosition(),
            XMLDoubleTongue(),
            XMLTripleTongue(),
            XMLStopped(),
            XMLSnapPizzicato(),
            XMLFret(0),
            XMLFret(1),
            XMLString(1),
            XMLString(5),
            [XMLHammerOn(type='start'), XMLHammerOn(type='stop')],
            [XMLPullOff(type='start'), XMLPullOff(type='stop')]
        ]

        bends = [XMLBend() for _ in range(4)]
        bends[0].add_child(XMLBendAlter(3))
        bends[1].add_child(XMLBendAlter(3))
        bends[1].add_child(XMLWithBar())
        bends[2].add_child(XMLBendAlter(0.5))
        bends[2].add_child(XMLPreBend())
        bends[3].add_child(XMLBendAlter(3.5))
        bends[3].add_child(XMLRelease())

        xml_notations += bends

        xml_notations += [
            XMLTap(),
            XMLTap(hand='left'),
            XMLHeel(),
            XMLToe(),
            XMLFingernails(),
            None,
            None,
            None,
            XMLF(),
            XMLPpp(),
            XMLSfp(),
            XMLOtherDynamics('sfffz'),
            (XMLStrongAccent(), XMLStaccato()),
        ]

        for n in xml_notations:
            if n is None:
                ch = Chord(0, 1)
                part.add_chord(ch)
            elif isinstance(n, XMLNonArpeggiate):
                ch = Chord([C(5), E(5), G(5)], 1)
                ch.add_lyric('XMLNonArpeggiate not implemented')
                part.add_chord(ch)
            elif isinstance(n, XMLArpeggiate):
                ch = Chord([C(5), E(5), G(5)], 1)
                ch.add_x(n)
                part.add_chord(ch)
            elif isinstance(n, XMLAccidentalMark):
                ch = Chord(C(5), 1)
                ch.add_x(n, parent_type='notation')
                part.add_chord(ch)
            elif isinstance(n, list):
                for x in n:
                    ch = Chord(C(5), 1)
                    ch.add_x(x)
                    part.add_chord(ch)
            elif isinstance(n, tuple):
                ch = Chord(C(5), 1)
                for x in n:
                    if isinstance(x, XMLAccidentalMark):
                        ch.add_x(x, parent_type='ornament')
                    else:
                        ch.add_x(x)
                part.add_chord(ch)
            elif n.__class__ in XML_DYNAMIC_CLASSES:
                ch = Chord(C(5), 1)
                ch.add_x(n, parent_type='notation', placement='below')
                part.add_chord(ch)
            else:
                ch = Chord(C(5), 1)
                ch.add_x(n)
                part.add_chord(ch)

        objects = (XMLStaccato(), XMLAccent(), XMLTenuto())
        placements = ['above', 'below', 'below']
        ch = Chord(60, 1)
        for o, p in zip(objects, placements):
            ch.add_x(o, placement=p)
            # print(o.placement)
        part.add_chord(ch)

        xml_path = Path(__file__).with_suffix('.xml')
        score.export_xml(xml_path)
