from lxml import etree as et
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

    def _set_child(self, type_, tag, value):
        if value is not None and not isinstance(value, type_):
            value = type_(value)

        current_xml_children = self.dtd.get_current_xml_children()
        if value:
            for xml_child in current_xml_children:
                if isinstance(xml_child, type_):
                    self.dtd.remove_xml_child(xml_child)

            self.dtd.add_xml_child(value)

        name = '_' + replace_dash(tag)

        self.__setattr__(name, value)

    def reset_dtd(self):
        self.dtd = copy.copy(self._DTD)
        self.dtd._dtd_choices = None
        self.dtd._choice_index = 0
        self.dtd._current_choice = None
        self.dtd._xml_children = None

    def add_child(self, child):
        if not self.dtd:
            raise DTDError('_DTD is None. No Child can be added. ')
        self.dtd.add_xml_child(child)
        child._up = self
        return child

    def remove_child(self, child):
        current_xml_children = self.dtd.get_current_xml_children()
        if child:
            current_xml_children.remove(child)
        self.reset_dtd()

        for xml_child in current_xml_children:
            self.dtd.add_xml_child(xml_child)

    def close(self):
        if self.dtd:
            self.dtd.close()

    def get_children(self):
        if self.dtd:
            return self.dtd.get_current_xml_children()
        return []

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

    def to_string(self):
        self.close()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
