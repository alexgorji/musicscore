from unittest import TestCase

from musicxml.xsd.xsdindicators import xsd_group_class_names
from musicxml.xsd.xsdindicators import *


class TestXSDGroups(TestCase):
    def test_xsd_group_list(self):
        assert sorted(xsd_group_class_names) == ['XSDGroupAllMargins', 'XSDGroupBeatUnit', 'XSDGroupClef', 'XSDGroupDisplayStepOctave',
                                                 'XSDGroupDuration', 'XSDGroupEditorial', 'XSDGroupEditorialVoice',
                                                 'XSDGroupEditorialVoiceDirection', 'XSDGroupFootnote', 'XSDGroupFullNote',
                                                 'XSDGroupHarmonyChord', 'XSDGroupLayout', 'XSDGroupLeftRightMargins', 'XSDGroupLevel',
                                                 'XSDGroupMusicData', 'XSDGroupNonTraditionalKey', 'XSDGroupPartGroup',
                                                 'XSDGroupScoreHeader', 'XSDGroupScorePart', 'XSDGroupSlash', 'XSDGroupStaff',
                                                 'XSDGroupTimeSignature', 'XSDGroupTraditionalKey', 'XSDGroupTranspose', 'XSDGroupTuning',
                                                 'XSDGroupVirtualInstrumentData', 'XSDGroupVoice']

    def test_xsd_group_doc(self):
        assert XSDGroupEditorial.__doc__ == 'The editorial group specifies editorial information for a musical element.'

    def test_xsd_group_get_sequence(self):
        assert XSDGroupEditorial().sequence.elements == [('XMLFootnote', '0', '1'), ('XMLLevel', '0', '1')]

    def test_xsd_group_score_header_sequence(self):
        assert XSDGroupScoreHeader().sequence.elements == [('XMLWork', '0', '1'), ('XMLMovementNumber', '0', '1'), ('XMLMovementTitle',
                                                                                                                    '0', '1'),
                                                           ('XMLIdentification', '0', '1'), ('XMLDefaults', '0', '1'),
                                                           ('XMLCredit', '0', 'unbounded'), ('XMLPartList', '1', '1')]