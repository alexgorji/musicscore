from musicxml.util.core import find_all_xsd_children, get_complex_type_all_base_classes, convert_to_xsd_class_name, root1
from musicxml.xsd.xsdattribute import XSDAttribute
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement
from musicxml.exceptions import XSDAttributeRequiredException, XSDWrongAttribute
from musicxml.xsd.xsdindicators import XSDSequence, XSDChoice
from musicxml.xsd.xsdsimpletype import *
from musicxml.xsd.xsdattribute import *
from musicxml.xsd.xsdindicators import *


class XSDComplexType(XSDTreeElement):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._xsd_indicator = None

    @classmethod
    def check_attributes(cls, val_dict):
        required_attributes = [attribute for attribute in cls.get_xsd_attributes() if attribute.is_required]
        for required_attribute in required_attributes:
            if required_attribute.name not in val_dict:
                raise XSDAttributeRequiredException(f"{cls.__name__} requires attribute: {required_attribute.name}")

        for key in val_dict:
            if key not in [attribute.name for attribute in cls.get_xsd_attributes()]:
                raise XSDWrongAttribute
            attribute = [attribute for attribute in cls.get_xsd_attributes() if attribute.name == key][0]
            attribute(val_dict[key])

    @classmethod
    def get_xsd_attributes(cls):
        output = []
        if cls.XSD_TREE.get_simple_content_extension():
            for child in cls.XSD_TREE.get_simple_content_extension().get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        elif cls.XSD_TREE.get_complex_content():
            complex_content_extension = cls.XSD_TREE.get_complex_content_extension()
            complex_type_extension_base_class_name = convert_to_xsd_class_name(complex_content_extension.get_attributes()['base'],
                                                                               'complex_type')
            extension_base = eval(complex_type_extension_base_class_name)
            output.extend(extension_base.get_xsd_attributes())
            for child in complex_content_extension.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
            return output
        else:
            for child in cls.XSD_TREE.get_children():
                if child.tag == 'attribute':
                    output.append(XSDAttribute(child))
                elif child.tag == 'attributeGroup':
                    output.extend(eval(child.xsd_element_class_name).get_xsd_attributes())
        return output

    @classmethod
    def get_xsd_indicator(cls):
        def get_occurrences(ch):
            min_ = ch.get_attributes().get('minOccurs')
            max_ = ch.get_attributes().get('maxOccurs')
            return 1 if not min_ else int(min_), 1 if not max_ else 'unbounded' if max_ == 'unbounded' else int(max_)

        for child in cls.XSD_TREE.get_children():
            if child.tag == 'sequence':
                return XSDSequence(child), *get_occurrences(child)
            if child.tag == 'choice':
                return XSDChoice(child), *get_occurrences(child)
            if child.tag == 'group':
                return eval(convert_to_xsd_class_name(child.get_attributes()['ref'], 'group'))(), *get_occurrences(child)
            if child.tag == 'complexContent':
                return eval(convert_to_xsd_class_name(child.get_children()[0].get_attributes()['base'],
                                                      'complex_type')).get_xsd_indicator()

    @classmethod
    def value_is_required(cls):
        if cls.XSD_TREE.get_simple_content():
            return True
        else:
            return False


xsd_complex_type_class_names = []

"""
Creating all XSDComplexType classes
"""
for complex_type in find_all_xsd_children(tag='complexType'):
    xsd_tree = XSDTree(complex_type)
    class_name = xsd_tree.xsd_element_class_name
    base_classes = f"({', '.join(get_complex_type_all_base_classes(xsd_tree))}, )"
    attributes = """
    {
    '__doc__': xsd_tree.get_doc(), 
    'XSD_TREE': xsd_tree
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xsd_complex_type_class_names.append(class_name)

xsd_tree_score_partwise = XSDTree(root1.find(".//{*}element[@name='score-partwise']"))


class XSDComplexTypeScorePartwise(XSDComplexType):
    XSD_TREE = XSDTree(root1.findall(".//{*}element[@name='score-partwise']//{*}complexType")[0])


class XSDComplexTypePart(XSDComplexType):
    XSD_TREE = XSDTree(root1.findall(".//{*}element[@name='score-partwise']//{*}complexType")[1])


class XSDComplexTypeMeasure(XSDComplexType):
    XSD_TREE = XSDTree(root1.findall(".//{*}element[@name='score-partwise']//{*}complexType")[2])


xsd_complex_type_class_names.extend(['XSDComplexTypeScorePartwise', 'XSDComplexTypePart', 'XSDComplexTypeMeasure'])

# __all__ = xsd_complex_type_class_names
__all__ = ['XSDComplexTypeAccidental', 'XSDComplexTypeAccidentalMark',
           'XSDComplexTypeAccidentalText', 'XSDComplexTypeAccord',
           'XSDComplexTypeAccordionRegistration', 'XSDComplexTypeAppearance',
           'XSDComplexTypeArpeggiate', 'XSDComplexTypeArrow', 'XSDComplexTypeArticulations',
           'XSDComplexTypeAssess', 'XSDComplexTypeAttributes', 'XSDComplexTypeBackup',
           'XSDComplexTypeBarStyleColor', 'XSDComplexTypeBarline', 'XSDComplexTypeBarre',
           'XSDComplexTypeBass', 'XSDComplexTypeBassStep', 'XSDComplexTypeBeam',
           'XSDComplexTypeBeatRepeat', 'XSDComplexTypeBeatUnitTied', 'XSDComplexTypeBeater',
           'XSDComplexTypeBend', 'XSDComplexTypeBookmark', 'XSDComplexTypeBracket',
           'XSDComplexTypeBreathMark', 'XSDComplexTypeCaesura', 'XSDComplexTypeCancel',
           'XSDComplexTypeClef', 'XSDComplexTypeCoda', 'XSDComplexTypeCredit',
           'XSDComplexTypeDashes', 'XSDComplexTypeDefaults', 'XSDComplexTypeDegree',
           'XSDComplexTypeDegreeAlter', 'XSDComplexTypeDegreeType',
           'XSDComplexTypeDegreeValue', 'XSDComplexTypeDirection',
           'XSDComplexTypeDirectionType', 'XSDComplexTypeDistance', 'XSDComplexTypeDouble',
           'XSDComplexTypeDynamics', 'XSDComplexTypeEffect', 'XSDComplexTypeElision',
           'XSDComplexTypeEmpty', 'XSDComplexTypeEmptyFont', 'XSDComplexTypeEmptyLine',
           'XSDComplexTypeEmptyPlacement', 'XSDComplexTypeEmptyPlacementSmufl',
           'XSDComplexTypeEmptyPrintObjectStyleAlign', 'XSDComplexTypeEmptyPrintStyle',
           'XSDComplexTypeEmptyPrintStyleAlign', 'XSDComplexTypeEmptyPrintStyleAlignId',
           'XSDComplexTypeEmptyTrillSound', 'XSDComplexTypeEncoding', 'XSDComplexTypeEnding',
           'XSDComplexTypeExtend', 'XSDComplexTypeFeature', 'XSDComplexTypeFermata',
           'XSDComplexTypeFigure', 'XSDComplexTypeFiguredBass', 'XSDComplexTypeFingering',
           'XSDComplexTypeFirstFret', 'XSDComplexTypeForPart', 'XSDComplexTypeFormattedSymbol',
           'XSDComplexTypeFormattedSymbolId', 'XSDComplexTypeFormattedText',
           'XSDComplexTypeFormattedTextId', 'XSDComplexTypeForward', 'XSDComplexTypeFrame',
           'XSDComplexTypeFrameNote', 'XSDComplexTypeFret', 'XSDComplexTypeGlass',
           'XSDComplexTypeGlissando', 'XSDComplexTypeGlyph', 'XSDComplexTypeGrace',
           'XSDComplexTypeGroupBarline', 'XSDComplexTypeGroupName',
           'XSDComplexTypeGroupSymbol', 'XSDComplexTypeGrouping',
           'XSDComplexTypeHammerOnPullOff', 'XSDComplexTypeHandbell',
           'XSDComplexTypeHarmonClosed', 'XSDComplexTypeHarmonMute', 'XSDComplexTypeHarmonic',
           'XSDComplexTypeHarmony', 'XSDComplexTypeHarmonyAlter', 'XSDComplexTypeHarpPedals',
           'XSDComplexTypeHeelToe', 'XSDComplexTypeHole', 'XSDComplexTypeHoleClosed',
           'XSDComplexTypeHorizontalTurn', 'XSDComplexTypeIdentification',
           'XSDComplexTypeImage', 'XSDComplexTypeInstrument', 'XSDComplexTypeInstrumentChange',
           'XSDComplexTypeInstrumentLink', 'XSDComplexTypeInterchangeable',
           'XSDComplexTypeInversion', 'XSDComplexTypeKey', 'XSDComplexTypeKeyAccidental',
           'XSDComplexTypeKeyOctave', 'XSDComplexTypeKind', 'XSDComplexTypeLevel',
           'XSDComplexTypeLineDetail', 'XSDComplexTypeLineWidth', 'XSDComplexTypeLink',
           'XSDComplexTypeListen', 'XSDComplexTypeListening', 'XSDComplexTypeLyric',
           'XSDComplexTypeLyricFont', 'XSDComplexTypeLyricLanguage', 'XSDComplexTypeMeasure',
           'XSDComplexTypeMeasureLayout', 'XSDComplexTypeMeasureNumbering',
           'XSDComplexTypeMeasureRepeat', 'XSDComplexTypeMeasureStyle',
           'XSDComplexTypeMembrane', 'XSDComplexTypeMetal', 'XSDComplexTypeMetronome',
           'XSDComplexTypeMetronomeBeam', 'XSDComplexTypeMetronomeNote',
           'XSDComplexTypeMetronomeTied', 'XSDComplexTypeMetronomeTuplet',
           'XSDComplexTypeMidiDevice', 'XSDComplexTypeMidiInstrument',
           'XSDComplexTypeMiscellaneous', 'XSDComplexTypeMiscellaneousField',
           'XSDComplexTypeMordent', 'XSDComplexTypeMultipleRest', 'XSDComplexTypeNameDisplay',
           'XSDComplexTypeNonArpeggiate', 'XSDComplexTypeNotations', 'XSDComplexTypeNote',
           'XSDComplexTypeNoteSize', 'XSDComplexTypeNoteType', 'XSDComplexTypeNotehead',
           'XSDComplexTypeNoteheadText', 'XSDComplexTypeNumeral', 'XSDComplexTypeNumeralKey',
           'XSDComplexTypeNumeralRoot', 'XSDComplexTypeOctaveShift', 'XSDComplexTypeOffset',
           'XSDComplexTypeOpus', 'XSDComplexTypeOrnaments', 'XSDComplexTypeOtherAppearance',
           'XSDComplexTypeOtherDirection', 'XSDComplexTypeOtherListening',
           'XSDComplexTypeOtherNotation', 'XSDComplexTypeOtherPlacementText',
           'XSDComplexTypeOtherPlay', 'XSDComplexTypeOtherText', 'XSDComplexTypePageLayout',
           'XSDComplexTypePageMargins', 'XSDComplexTypePart', 'XSDComplexTypePartClef',
           'XSDComplexTypePartGroup', 'XSDComplexTypePartLink', 'XSDComplexTypePartList',
           'XSDComplexTypePartName', 'XSDComplexTypePartSymbol', 'XSDComplexTypePartTranspose',
           'XSDComplexTypePedal', 'XSDComplexTypePedalTuning', 'XSDComplexTypePerMinute',
           'XSDComplexTypePercussion', 'XSDComplexTypePitch', 'XSDComplexTypePitched',
           'XSDComplexTypePlacementText', 'XSDComplexTypePlay', 'XSDComplexTypePlayer',
           'XSDComplexTypePrincipalVoice', 'XSDComplexTypePrint', 'XSDComplexTypeRelease',
           'XSDComplexTypeRepeat', 'XSDComplexTypeRest', 'XSDComplexTypeRoot',
           'XSDComplexTypeRootStep', 'XSDComplexTypeScaling', 'XSDComplexTypeScordatura',
           'XSDComplexTypeScoreInstrument', 'XSDComplexTypeScorePart',
           'XSDComplexTypeScorePartwise', 'XSDComplexTypeSegno', 'XSDComplexTypeSlash',
           'XSDComplexTypeSlide', 'XSDComplexTypeSlur', 'XSDComplexTypeSound',
           'XSDComplexTypeStaffDetails', 'XSDComplexTypeStaffDivide',
           'XSDComplexTypeStaffLayout', 'XSDComplexTypeStaffSize', 'XSDComplexTypeStaffTuning',
           'XSDComplexTypeStem', 'XSDComplexTypeStick', 'XSDComplexTypeString',
           'XSDComplexTypeStringMute', 'XSDComplexTypeStrongAccent', 'XSDComplexTypeStyleText',
           'XSDComplexTypeSupports', 'XSDComplexTypeSwing', 'XSDComplexTypeSync',
           'XSDComplexTypeSystemDividers', 'XSDComplexTypeSystemLayout',
           'XSDComplexTypeSystemMargins', 'XSDComplexTypeTap', 'XSDComplexTypeTechnical',
           'XSDComplexTypeTextElementData', 'XSDComplexTypeTie', 'XSDComplexTypeTied',
           'XSDComplexTypeTime', 'XSDComplexTypeTimeModification', 'XSDComplexTypeTimpani',
           'XSDComplexTypeTranspose', 'XSDComplexTypeTremolo', 'XSDComplexTypeTuplet',
           'XSDComplexTypeTupletDot', 'XSDComplexTypeTupletNumber',
           'XSDComplexTypeTupletPortion', 'XSDComplexTypeTupletType',
           'XSDComplexTypeTypedText', 'XSDComplexTypeUnpitched',
           'XSDComplexTypeVirtualInstrument', 'XSDComplexTypeWait', 'XSDComplexTypeWavyLine',
           'XSDComplexTypeWedge', 'XSDComplexTypeWood', 'XSDComplexTypeWork']
