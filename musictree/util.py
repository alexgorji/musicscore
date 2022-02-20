import math
from typing import Union, List
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
              (1, 4): '16th',
              (2, 4): 'eighth',
              (3, 4): 'eighth',
              (7, 4): 'quarter',
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


def lcm(l):
    return math.lcm(*l)


XML_ARTICULATION_CLASSES = [XMLAccent, XMLStrongAccent, XMLStaccato, XMLTenuto, XMLDetachedLegato, XMLStaccatissimo,
                            XMLSpiccato, XMLScoop, XMLPlop, XMLDoit, XMLFalloff, XMLBreathMark, XMLCaesura, XMLStress,
                            XMLUnstress]

XML_TECHNICAL_CLASSES = [XMLUpBow, XMLDownBow, XMLHarmonic, XMLOpenString, XMLThumbPosition, XMLFingering, XMLPluck, XMLDoubleTongue,
                         XMLTripleTongue, XMLStopped, XMLSnapPizzicato, XMLFret, XMLString, XMLHammerOn, XMLPullOff, XMLBend, XMLTap,
                         XMLHeel, XMLToe, XMLFingernails, XMLHole, XMLArrow, XMLHandbell, XMLBrassBend, XMLFlip, XMLSmear, XMLOpen,
                         XMLHalfMuted, XMLHarmonMute, XMLGolpe, XMLOtherTechnical]
