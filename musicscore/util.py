import math
from typing import Union, List

from musicscore.exceptions import WrongNumberOfChordsError, LyricSyllabicOrExtensionError
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

#:
XML_ARTICULATION_CLASSES = [XMLAccent, XMLStrongAccent, XMLStaccato, XMLTenuto, XMLDetachedLegato, XMLStaccatissimo,
                            XMLSpiccato, XMLScoop, XMLPlop, XMLDoit, XMLFalloff, XMLBreathMark, XMLCaesura, XMLStress,
                            XMLUnstress]

#:
XML_TECHNICAL_CLASSES = [XMLUpBow, XMLDownBow, XMLHarmonic, XMLOpenString, XMLThumbPosition, XMLFingering, XMLPluck,
                         XMLDoubleTongue,
                         XMLTripleTongue, XMLStopped, XMLSnapPizzicato, XMLFret, XMLString, XMLHammerOn, XMLPullOff,
                         XMLBend, XMLTap,
                         XMLHeel, XMLToe, XMLFingernails, XMLHole, XMLArrow, XMLHandbell, XMLBrassBend, XMLFlip,
                         XMLSmear, XMLOpen,
                         XMLHalfMuted, XMLHarmonMute, XMLGolpe, XMLOtherTechnical]

#:
XML_ORNAMENT_CLASSES = [XMLDelayedInvertedTurn, XMLDelayedTurn, XMLHaydn, XMLInvertedMordent,
                        XMLInvertedTurn,
                        XMLInvertedVerticalTurn, XMLMordent, XMLOtherOrnament, XMLSchleifer, XMLShake, XMLTremolo,
                        XMLTrillMark, XMLTurn,
                        XMLVerticalTurn, XMLWavyLine]

#:
XML_DYNAMIC_CLASSES = [XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf,
                       XMLPp, XMLPpp, XMLPppp,
                       XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp,
                       XMLOtherDynamics]

#:
XML_OTHER_NOTATIONS = [XMLArpeggiate, XMLFermata, XMLFootnote, XMLGlissando, XMLLevel, XMLNonArpeggiate,
                       XMLOtherNotation, XMLSlide,
                       XMLSlur]

#:
XML_DIRECTION_TYPE_CLASSES = [
    XMLRehearsal, XMLSegno, XMLCoda, XMLWords, XMLSymbol, XMLWedge, XMLDashes, XMLBracket, XMLPedal,
    XMLMetronome, XMLOctaveShift, XMLHarpPedals, XMLDamp, XMLDampAll, XMLEyeglasses, XMLStringMute, XMLScordatura,
    XMLPrincipalVoice, XMLPercussion, XMLAccordionRegistration, XMLStaffDivide, XMLOtherDirection
]

#:
XML_ORNAMENT_AND_OTHER_NOTATIONS = [XMLAccidentalMark]

#:
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


def _chord_is_in_a_repetition(chord):
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


def trill_chords(chords, number=1, placement='above', **kwargs):
    if len(chords) < 2:
        raise WrongNumberOfChordsError('util.trill_chords needs at list two chords.')
    chords[0].add_x(XMLTrillMark(placement=placement, **kwargs))
    chords[0].add_x(XMLWavyLine(type='start', number=number, **kwargs), placement=placement)
    chords[-1].add_x(XMLWavyLine(type='stop', number=number, **kwargs), placement=placement)
    for ch in chords[1:-1]:
        ch.add_x(XMLWavyLine(type='continue', number=number, **kwargs), placement=placement)


def wedge_chords(chords, wedge_type, number=1, placement='below', **kwargs):
    if len(chords) < 2:
        raise WrongNumberOfChordsError('util.wedge_chords needs at list two chords.')

    chords[0].add_x(XMLWedge(type=wedge_type, number=number, **kwargs), placement=placement)
    chords[-1].add_x(XMLWedge(type='stop', number=number), placement=placement)
    for ch in chords[1:-1]:
        ch.add_x(XMLWedge(type='continue', number=number), placement=placement)


def bracket_chords(chords, line_type='solid', start_line_end='down', end_line_end='down', placement='above', number=1):
    if len(chords) < 2:
        raise WrongNumberOfChordsError('util.bracket_chords needs at list two chords.')

    chords[0].add_x(XMLBracket(type='start', line_end=start_line_end, line_type=line_type, number=number),
                    placement=placement)
    chords[-1].add_x(XMLBracket(type='stop', line_end=end_line_end, line_type=line_type, number=number),
                     placement=placement)
    for ch in chords[1:-1]:
        ch.add_x(XMLBracket(type='continue', line_end='none', line_type=line_type, number=number), placement=placement)


def octave_chords(chords, type='down', size=8, number=1):
    try:
        len(chords)
    except TypeError:
        chords = [chords]
    if type == 'down':
        placement = 'above'
    else:
        placement = 'below'

    chords[0].add_x(XMLOctaveShift(type=type, size=size, number=number), placement=placement)
    chords[-1].add_x(XMLOctaveShift(type='stop', size=size, number=number), placement=placement)
    for ch in chords[1:-1]:
        ch.add_x(XMLOctaveShift(type='continue', size=size, number=number), placement=placement)


def _generate_lyrics(lyrics, number=1, show_number=False, mode='list', **kwargs):
    def _get_syllables_extensions_from_group(syllabic_group):
        if syllabic_group[0] is None:
            raise LyricSyllabicOrExtensionError(
                f'Syllabic or extension cannot be added to the beginning of a syllabic group.')
        extensions_ = []
        syllables_ = list(syllabic_group)[:]
        while syllables_[-1] is None:
            extensions_.append(syllables_.pop())
        return [syllables_, extensions_]

    if isinstance(lyrics, str) or isinstance(lyrics, tuple):
        lyrics = [lyrics]

    output = []
    if mode == 'list':
        for i in range(len(lyrics)):
            ll = lyrics[i]
            if isinstance(ll, str):
                xl = XMLLyric(number=str(number), **kwargs)
                xl.xml_text = ll
                xl.xml_syllabic = 'single'
                output.append(xl)

            elif isinstance(ll, tuple) or isinstance(ll, list):
                syllables, extensions = _get_syllables_extensions_from_group(ll)
                if len(syllables) == 1:
                    xl = XMLLyric(number=str(number), **kwargs)
                    xl.xml_text = syllables[0]
                    xl.xml_syllabic = 'single'
                    if len(extensions) > 0:
                        xl.xml_extend = XMLExtend(type='start')

                    output.append(xl)
                else:
                    for j in range(len(syllables)):
                        xl = XMLLyric(number=str(number), **kwargs)
                        l = syllables[j]
                        if l:
                            xl.xml_text = l
                            if j == 0:
                                xl.xml_syllabic = 'begin'
                            elif j == len(syllables) - 1:
                                xl.xml_syllabic = 'end'
                                if len(extensions) > 0:
                                    xl.xml_extend = XMLExtend(type='start')
                            else:
                                xl.xml_syllabic = 'middle'
                        else:
                            xl = None
                        output.append(xl)

                for k in range(len(extensions)):
                    xl = XMLLyric(number=str(number), **kwargs)
                    if k == len(extensions) - 1:
                        xl.xml_extend = XMLExtend(type='stop')
                    else:
                        xl.xml_extend = XMLExtend(type='continue')
                    xl.xsd_check = False
                    output.append(xl)
            elif ll is None:
                output.append(None)
            else:
                raise NotImplementedError(ll)
    else:
        raise NotImplementedError
    if show_number:
        first = XMLLyric(**kwargs)
        for k, i in output[0].attributes.items():
            setattr(first, k, i)
        first.add_child(XMLSyllabic('single'))
        first.add_child(XMLText(f'{number}.'))
        first.add_child(XMLElision(' '))

        for child in output[0].get_children():
            first.add_child(child)

        output[0] = first
    return output

def split_list(original_list, split_indices):
    if not split_indices:
        return [original_list]
    
    if split_indices[0] == 0:
        split_indices = split_indices[1:]

    return [original_list[i:j] for i, j in zip([0] + split_indices, split_indices + [None])]