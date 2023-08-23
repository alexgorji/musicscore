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

XML_ORNAMENT_CLASSES = [XMLAccidentalMark, XMLDelayedInvertedTurn, XMLDelayedTurn, XMLHaydn, XMLInvertedMordent,
                        XMLInvertedTurn,
                        XMLInvertedVerticalTurn, XMLMordent, XMLOtherOrnament, XMLSchleifer, XMLShake, XMLTremolo,
                        XMLTrillMark, XMLTurn,
                        XMLVerticalTurn, XMLWavyLine]

XML_DYNAMIC_CLASSES = [XMLF, XMLFf, XMLFff, XMLFfff, XMLFffff, XMLFfffff, XMLFp, XMLFz, XMLMf, XMLMp, XMLP, XMLPf,
                       XMLPp, XMLPpp, XMLPppp,
                       XMLPpppp, XMLPppppp, XMLRf, XMLRfz, XMLSf, XMLSffz, XMLSfp, XMLSfpp, XMLSfz, XMLSfzp]

XML_OTHER_NOTATIONS = [XMLArpeggiate, XMLFermata, XMLFootnote, XMLGlissando, XMLLevel, XMLNonArpeggiate,
                       XMLOtherNotation, XMLSlide,
                       XMLSlur]
