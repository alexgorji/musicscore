from lxml import etree as et
import warnings

from musicscore.basic_functions import replace_dash
from musicscore.musicxml.exceptions import AfterInitializationError, ChildAlreadyExists
from musicscore.tree.tree import Tree


class XMLElement(Tree):
    _ATTRIBUTES = (
        'id', 'part-name', 'number', 'location', 'print-object', 'default-x', 'default-y', 'relative-x', 'relative-y',
        'font-family', 'font-size', 'font-weight', 'font-style', 'color')
    _CHILDREN_TYPES = []
    _CHILDREN_ORDERED = False

    def __init__(self, tag, *args, **kwargs):
        self._attributes = {}
        self._tag = None
        self.tag = tag
        super().__init__(*args, **kwargs)
        self._text = None
        self._test_mode = None
        self._multiple = False

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

    @property
    def test_mode(self):
        if self._test_mode is None:
            if not self.is_root():
                return self.up.test_mode
            else:
                return False
        else:
            return self._test_mode

    @test_mode.setter
    def test_mode(self, value):
        """
        If test_mode is True children will appear without text and attributes.
        Default is False.
        """
        if value is not None and not isinstance(value, bool):
            raise TypeError('test mode must be boolean or None')
        self._test_mode = value

    @property
    def multiple(self):
        return self._multiple

    @multiple.setter
    def multiple(self, value):
        if not isinstance(value, bool):
            raise TypeError('multiple.value must be of type bool not{}'.format(type(value)))
        self._multiple = value

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

    def _sort_attributes(self):
        def sort_function(x):
            return self._ATTRIBUTES.index(x)

        sorted_attributes = {}
        for key in sorted(self._attributes, key=sort_function):
            sorted_attributes[key] = self._attributes[key]
        self._attributes = sorted_attributes

    def set_attribute(self, attribute_name, attribute_value):

        if attribute_name not in self._ATTRIBUTES:
            raise ValueError('{}.set_attribute: attribute_name: {} is not in XMLElement._ATTRIBUTES'.format(type(self),
                                                                                                            attribute_name))
        self.get_attributes()[attribute_name] = attribute_value
        self._sort_attributes()

    def remove_attribute(self, attribute):
        if attribute in self.get_attributes().keys():
            self.get_attributes().pop(attribute)

    def clear_attributes(self):
        self.get_attributes().clear()

    def __repr__(self):
        return '{} instance {} at {}'.format(self.__class__.__name__, self.tag, hex(id(self)))

    def _check_childtype(self, child):
        _type_error = True
        for child_type in self._CHILDREN_TYPES:
            if isinstance(child, child_type):
                _type_error = False
                break
        if _type_error is True:
            raise TypeError('child can only be of type(s): {} not {}'.format(self._CHILDREN_TYPES, type(child)))

    def get_children_by_type(self, type_):
        return [child for child in self.get_children() if isinstance(child, type_)]

    def get_children_by_tag(self, tag):
        return [child for child in self.get_children() if child.tag == tag]

    def _check_multiple_children(self, child):
        if child.multiple is False:
            existing_children = self.get_children_by_type(type(child))
            if len(existing_children) != 0:
                raise ChildAlreadyExists(child)

    def add_child(self, child):
        self._check_childtype(child)
        self._check_multiple_children(child)
        self._children.append(child)
        child._up = self
        return child

    def find_child_by_tag(self, tag):
        return next((child for child in self._children if child.tag == tag), None)

    def find_child_by_type(self, type):
        return next((child for child in self._children if isinstance(child, type)), None)

    def remove_old_child_by_tag(self, tag):
        old_child = self.find_child_by_tag(tag)
        if old_child is not None:
            self.remove_child(old_child)

    def remove_old_child_by_type(self, type):
        old_child = self.find_child_by_type(type)
        if old_child is not None:
            self.remove_child(old_child)

    def replace_old_child_by_tag(self, tag, new_child):
        self.remove_old_child_by_tag(tag)
        if new_child is not None:
            if new_child.tag != tag:
                raise ValueError('new_child must have the tag {}'.format(tag))
            self.add_child(new_child)

    def replace_old_child_by_type(self, type, new_child):
        self.remove_old_child_by_type(type)
        if new_child is not None:
            if not isinstance(new_child, type):
                raise ValueError('new_child must be of type {}'.format(type))
            self.add_child(new_child)

    def _sort_children(self):
        sorted_ = []

        for child_type in self._CHILDREN_TYPES:
            child_list = self.get_children_by_type(child_type)
            for child in child_list:
                sorted_.append(child)
                self._children.remove(child)

        if len(self._children) != 0:
            warnings.warn(
                'length of sorted children of {} is smaller than its children. Remaining not sorted children are: {}'.format(
                    self, self._children))

        sorted_.extend(self._children)
        self._children = sorted_

    def _to_xml(self):
        if self._CHILDREN_ORDERED is True:
            self._sort_children()
        xml = et.Element(_tag=self.tag)

        def set_attributes():
            for key in self.get_attributes().keys():
                xml.set(key, str(self.get_attributes()[key]))

        def set_children():
            for child in self.get_children():
                if isinstance(child, XMLElement):
                    xml.append(child._to_xml())
                elif isinstance(child, XMLElementGroup):
                    for sibling in child:
                        xml.append(sibling._to_xml())
                else:
                    raise TypeError('child {} must be of type XMLElement or XMLElementgroup'.format(child))

        set_children()

        # todo
        if self.test_mode is False:
            if self.text is not None:
                xml.text = str(self.text)
            set_attributes()

        return xml

    def _set_child(self, type_, tag, value):

        if value is not None and not isinstance(value, type_):
            value = type_(value)

        self.replace_old_child_by_tag(tag=tag, new_child=value)

        name = '_' + replace_dash(tag)

        self.__setattr__(name, value)

    def to_string(self):
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
