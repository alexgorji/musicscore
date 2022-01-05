from musicxml.util.core import cap_first, find_all_xsd_children, convert_to_xml_class_name
from musicxml.xsd.xsdtree import XSDTree, XSDTreeElement


class XSDSequence:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self._elements = None
        self.xsd_tree = xsd_tree

    @property
    def elements(self):
        if not self._elements:
            self._elements = []
            for child in self.xsd_tree.get_children():
                if child.tag == 'element':
                    element = convert_to_xml_class_name(child.name)
                    min_occurrence = child.get_attributes().get('minOccurs')
                    if min_occurrence is None: min_occurrence = '1'
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if max_occurrence is None: max_occurrence = '1'
                    self._elements.append((element, min_occurrence, max_occurrence))

                elif child.tag == 'group':
                    xsd_group_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in child.get_attributes()['ref'].split('-')])
                    elements = eval(xsd_group_name)().sequence.elements
                    min_occurrence = child.get_attributes().get('minOccurs')
                    max_occurrence = child.get_attributes().get('maxOccurs')
                    if min_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[1] = min_occurrence
                        elements[0] = tuple(list_el)
                    if max_occurrence is not None:
                        if len(elements) > 1:
                            raise NotImplementedError
                        list_el = list(elements[0])
                        list_el[2] = max_occurrence
                        elements[0] = tuple(list_el)
                    self._elements.extend(elements)
                else:
                    raise NotImplementedError(child.tag)
        return self._elements

    @property
    def required_elements(self):
        return [el[0] for el in self.elements if el[1] == '1']

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'sequence':
            raise ValueError
        self._xsd_tree = value

    def order_elements(self, elements):
        return elements


class XSDChoice:
    def __init__(self, xsd_tree):
        self._xsd_tree = None
        self.xsd_tree = xsd_tree

    @property
    def xsd_tree(self):
        return self._xsd_tree

    @xsd_tree.setter
    def xsd_tree(self, value):
        if not isinstance(value, XSDTree):
            raise TypeError
        if value.tag != 'choice':
            raise ValueError
        self._xsd_tree = value


class XSDGroup(XSDTreeElement):

    def __init__(self):
        self._sequence = None
        self._name = None

    @property
    def name(self):
        return self.XSD_TREE.name

    @property
    def sequence(self):
        if not self._sequence:
            for child in self.XSD_TREE.get_children():
                if child.tag == 'sequence':
                    self._sequence = XSDSequence(child)
        return self._sequence


xsd_group_class_names = []
xsd_groups = find_all_xsd_children(tag='group')

for xsd_group in xsd_groups:
    xsd_tree = XSDTree(xsd_group)
    class_name = 'XSDGroup' + ''.join([cap_first(partial) for partial in xsd_tree.name.split('-')])
    base_classes = "(XSDGroup, )"
    attributes = """
    {
    'XSD_TREE': xsd_tree,
    '__doc__': xsd_tree.get_doc()
    }
    """
    exec(f"{class_name} = type('{class_name}', {base_classes}, {attributes})")
    xsd_group_class_names.append(class_name)

# __all__ = xsd_group_class_names
__all__ = ['XSDGroupAllMargins', 'XSDGroupBeatUnit', 'XSDGroupClef', 'XSDGroupDisplayStepOctave',
           'XSDGroupDuration', 'XSDGroupEditorial', 'XSDGroupEditorialVoice',
           'XSDGroupEditorialVoiceDirection', 'XSDGroupFootnote', 'XSDGroupFullNote',
           'XSDGroupHarmonyChord', 'XSDGroupLayout', 'XSDGroupLeftRightMargins', 'XSDGroupLevel',
           'XSDGroupMusicData', 'XSDGroupNonTraditionalKey', 'XSDGroupPartGroup',
           'XSDGroupScoreHeader', 'XSDGroupScorePart', 'XSDGroupSlash', 'XSDGroupStaff',
           'XSDGroupTimeSignature', 'XSDGroupTraditionalKey', 'XSDGroupTranspose', 'XSDGroupTuning',
           'XSDGroupVirtualInstrumentData', 'XSDGroupVoice']
