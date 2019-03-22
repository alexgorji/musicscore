from lxml import etree as et
import warnings
import copy

from musicscore.basic_functions import replace_dash
from musicscore.dtd.dtd import DTDError
from musicscore.musicxml.exceptions import AfterInitializationError
from musicscore.tree.tree import Tree


class XMLTree(Tree):
    _DTD = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtd = copy.copy(self._DTD)

        self._sorted = False
        self._sorted_children = []

    def find_child_by_tag(self, tag):
        return next((child for child in self._children if child.tag == tag), None)

    def remove_old_child_by_tag(self, tag):
        old_child = self.find_child_by_tag(tag)
        if old_child is not None:
            self.remove_child(old_child)

    def replace_old_child_by_tag(self, tag, new_child):
        self.remove_old_child_by_tag(tag)
        if new_child is not None:
            if new_child.tag != tag:
                raise ValueError('new_child must have the tag {}'.format(tag))
            self.add_child(new_child)

    def _set_child(self, type_, tag, value):

        if value is not None and not isinstance(value, type_):
            value = type_(value)

        self.replace_old_child_by_tag(tag=tag, new_child=value)

        name = '_' + replace_dash(tag)

        self.__setattr__(name, value)

    def add_child(self, child):
        if not self.dtd:
            raise DTDError('_DTD is None. No Child can be added. ')
        self.dtd.check_child_type(self, child)
        self.dtd.check_child_max_occurrence(self, child)
        self._children.append(child)
        child._up = self
        return child

    def sort_children(self):
        self.dtd.reduce_group_references()
        current_combination = self.dtd.get_current_combination()
        common_ancestor = current_combination[0].get_common_ancestor(*current_combination[1:])
        self._sorted_children = []
        common_ancestor.sort_children(self)
        self._children = self._sorted_children

    def close(self):
        if self.dtd:
            self.dtd.close(self)
        for child in self.get_children():
            child.close()

    def get_children_by_type(self, type_):
        return [child for child in self.get_children() if isinstance(child, type_)]


class XMLElement(XMLTree):
    _ATTRIBUTES = None

    def __init__(self, tag, *args, **kwargs):
        self._attributes = {}
        self._tag = None
        self.tag = tag
        super().__init__(*args, **kwargs)
        self._text = None

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        if self._tag is not None:
            raise AfterInitializationError(self.tag)
        self._tag = value

    @property
    def text(self):
        try:
            return self.value
        except AttributeError:
            return self._text

    @text.setter
    def text(self, v):
        try:
            self.value = v
        except AttributeError:
            self._text = v

    def __getattr__(self, item):
        tag = replace_dash(item)
        found_children = self.get_children_by_tag(tag)
        if len(found_children) == 0:
            raise AttributeError('object "{}" has no attribute "{}"'.format(type(self).__name__, item))

        if len(found_children) == 1:
            return found_children[0]
        else:
            return found_children

    def get_attributes(self):
        return self._attributes

    def get_attribute(self, attribute_name):
        return self.get_attributes()[attribute_name]

    def get_children_by_tag(self, tag):
        return [child for child in self.get_children() if child.tag == tag]

    def _sort_attributes(self):
        def sort_function(x):
            return self._ATTRIBUTES.index(x)

        sorted_attributes = {}
        for key in sorted(self._attributes, key=sort_function):
            sorted_attributes[key] = self._attributes[key]
        self._attributes = sorted_attributes

    def set_attribute(self, attribute_name, attribute_value):
        if self._ATTRIBUTES is not None:
            if attribute_name not in self._ATTRIBUTES:
                raise ValueError('{}.set_attribute: attribute_name: {} is not in {}._ATTRIBUTES'.format(type(self),
                                                                                                        attribute_name,
                                                                                                        self.__class__.__name__))
        self.get_attributes()[attribute_name] = attribute_value
        if self._ATTRIBUTES is not None:
            self._sort_attributes()

    def remove_attribute(self, attribute):
        if attribute in self.get_attributes().keys():
            self.get_attributes().pop(attribute)

    def clear_attributes(self):
        self.get_attributes().clear()

    def __repr__(self):
        try:
            return '{} {} at {}'.format(self.__class__.__name__, self.value, hex(id(self)))
        except AttributeError:
            return '{} at {}'.format(self.__class__.__name__, hex(id(self)))

    def _to_xml(self):

        # self.sort_children()
        xml = et.Element(_tag=self.tag)

        def set_attributes():
            for key in self.get_attributes().keys():
                xml.set(key, str(self.get_attributes()[key]))

        def set_children():
            for child in self.get_children():
                if isinstance(child, XMLElement):
                    xml.append(child._to_xml())
                else:
                    raise TypeError('child {} must be of type XMLElement2 or XMLElementGroup'.format(child))

        set_children()
        if self.text is not None:
            xml.text = str(self.text)
        set_attributes()
        return xml

    def reset_children(self):
        self.clear_children()
        self.dtd._possibility_index = 0

    def to_string(self):
        self.close()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
