import math
from typing import Union, List

from musictree.exceptions import WrongNumberOfChordsError
from musicxml.xmlelement.xmlelement import *

note_types = {(1, 12): '32nd',
              (1, 11): '32nd',
              (2, 11): '16th',
              (3, 11): '16th',
              (4, 11): 'eighth',
              (6, 11): 'eighth',
              (8, 11): 'quarter',
              (1, 10): '32nd',
              (3, 10): '16th',
              (1, 9): '32nd',
              (2, 9): '16th',
              (4, 9): 'eighth',
              (8, 9): 'quarter',
              (1, 8): '32nd',
              (3, 8): '16th',
              (7, 8): 'eighth',
              (1, 7): '16th',
              (2, 7): 'eighth',
              (3, 7): 'eighth',
              (4, 7): 'quarter',
              (6, 7): 'quarter',
              (1, 6): '16th',
              (1, 5): '16th',
              (2, 5): 'eighth',
              (3, 5): 'eighth',
              (4, 5): 'quarter',
              (6, 5): 'quarter',
              (8, 5): 'half',
              (1, 4): '16th',
              (2, 4): 'eighth',
              (3, 4): 'eighth',
              (7, 4): 'quarter',
              (4, 3): 'half',
              (1, 3): 'eighth',
              (2, 3): 'quarter',
              (3, 2): 'quarter',
              (1, 2): 'eighth',
              (1, 1): 'quarter',
              (2, 1): 'half',
              (3, 1): 'half',
              (4, 1): 'whole',
              (6, 1): 'whole',
              (8, 1): 'breve',
              (12, 1): 'breve'
              }

XML_ARTICULATION_CLASSES = [XMLAccent, XMLStrongAccent, XMLStaccato, XMLTenuto, XMLDetachedLegato, XMLStaccatissimo,
                            XMLSpiccato, XMLScoop, XMLPlop, XMLDoit, XMLFalloff, XMLBreathMark, XMLCaesura, XMLStress,
                            XMLUnstress]

XML_TECHNICAL_CLASSES = [XMLUpBow, XMLDownBow, XMLHarmonic, XMLOpenString, XMLThumbPosition, XMLFingering, XMLPluck,
                         XMLDoubleTongue,
                         XMLTripleTongue, XMLStopped, XMLSnapPizzicato, XMLFret, XMLString, XMLHammerOn, XMLPullOff,
                         XMLBend, XMLTap,
                         XMLHeel, XMLToe, XMLFingernails, XMLHole, XMLArrow, XMLHandbell, XMLBrassBend, XMLFlip,
                         XMLSmear, XMLOpen,
                         XMLHalfMuted, XMLHarmonMute, XMLGolpe, XMLOtherTechnical]

XML_ORNAMENT_CLASSES = [XMLDelayedInvertedTurn, XMLDelayedTurn, XMLHaydn, XMLInvertedMordent,
                        XMLInvertedTurn,
                        XMLInvertedVerticalTurn, XMLMordent, XMLOtherOrnament, XMLSchleifer, XMLShake, XMLTremolo,
                        XMLTrillMark, XMLTurn,
                        XMLVerticalTurn, XMLWavyLine]

XML_DYNAMIC_CLASSES = [XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf,
                       XMLPp, XMLPpp, XMLPppp,
                       XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp,
                       XMLOtherDynamics]

XML_OTHER_NOTATIONS = [XMLArpeggiate, XMLFermata, XMLFootnote, XMLGlissando, XMLLevel, XMLNonArpeggiate,
                       XMLOtherNotation, XMLSlide,
                       XMLSlur]

# XML_DIRECTION_TYPE_CLASSES = [
#     XMLRehearsal, XMLSegno, XMLCoda, XMLWords, XMLSymbol, XMLWedge, XMLDashes, XMLBracket, XMLPedal,
#     XMLMetronome, XMLOctaveShift, XMLHarpPedals, XMLDamp, XMLDampAll, XMLEyeglasses, XMLStringMute, XMLScordatura,
#     XMLImage, XMLPrincipalVoice, XMLPercussion, XMLAccordionRegistration, XMLStaffDivide, XMLOtherDirection
# ]

XML_DIRECTION_TYPE_CLASSES = [
    XMLRehearsal, XMLSegno, XMLCoda, XMLWords, XMLSymbol, XMLWedge, XMLDashes, XMLBracket, XMLPedal,
    XMLMetronome, XMLOctaveShift, XMLHarpPedals, XMLDamp, XMLDampAll, XMLEyeglasses, XMLStringMute, XMLScordatura,
    XMLPrincipalVoice, XMLPercussion, XMLAccordionRegistration, XMLStaffDivide, XMLOtherDirection
]

XML_ORNAMENT_AND_OTHER_NOTATIONS = [XMLAccidentalMark]

XML_DIRECTION_TYPE_AND_OTHER_NOTATIONS = [XMLDynamics]


def lcm(l):
    return math.lcm(*l)


def dToX(input_list, first_element=0):
    if isinstance(input_list, list) is False:
        raise TypeError('xToD(input_list)')
    else:
        output = [first_element]
        for i in range(len(input_list)):
            output.append(input_list[i] + output[i])
        return output


def xToD(input_list):
    result = []
    for i in range(1, len(input_list)):
        result.append(input_list[i] - input_list[i - 1])
    return result


def isinstance_as_string(child: object, parent_class_names: Union[str, List[str]]) -> bool:
    """
    This function can be used to check if some class names (parent_class_names) can be found in another class's __mro__.
    If parent classes cannot be imported due to recursive imports this can be used instead of isinstance function.
    :param object child:
    :param str/[str] parent_class_names:
    :return: bool
    """
    if isinstance(parent_class_names, str):
        parent_class_names = [parent_class_names]

    for parent_class_name in parent_class_names:
        if parent_class_name not in [cls.__name__ for cls in child.__class__.__mro__]:
            return False
    return True


def chord_is_in_a_repetition(chord):
    my_index = chord.up.up.get_chords().index(chord)
    if my_index > 0 and not chord.is_tied_to_previous:
        all_previous_chords = [chord.up.up.get_chords()[my_index - i] for i in range(1, my_index + 1)]
        if set([ch.is_tied_to_previous for ch in all_previous_chords]) == {True}:
            return False
        previous_chord = all_previous_chords[0]
        if chord.has_same_pitches(previous_chord):
            return True
    return False


def slur_chords(chords, number=1, **kwargs):
    if len(chords) < 2:
        raise WrongNumberOfChordsError('util.slur_chords needs at list two chords.')

    chords[0].add_x(XMLSlur(type='start', number=number, **kwargs))
    chords[-1].add_x(XMLSlur(type='stop', number=number))
    for ch in chords[1:-1]:
        ch.add_x(XMLSlur(type='continue', number=number))


def wedge_chords(chords, wedge_type, number=1, placement='below', **kwargs):
    if len(chords) < 2:
        raise WrongNumberOfChordsError('util.wedge_chords needs at list two chords.')

    chords[0].add_x(XMLWedge(type=wedge_type, number=number, **kwargs), placement=placement)
    chords[-1].add_x(XMLWedge(type='stop', number=number), placement=placement)
    for ch in chords[1:-1]:
        ch.add_x(XMLWedge(type='continue', number=number), placement=placement)