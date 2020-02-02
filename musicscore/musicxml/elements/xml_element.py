from lxml import etree as et

from musicscore.basic_functions import replace_dash
from musicscore.dtd.dtd import DTDError, ChildIsNotOptional, ChildTypeDTDConflict, ChildOccurrenceDTDConflict, Sequence
from musicscore.musicxml.exceptions import AfterInitializationError
from musicscore.tree.tree import Tree


class XMLTree(Tree):
    _DTD = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtd = self._DTD
        self._current_children = []
        self._current_choice = None
        self._choice_index = 0
        self._old_choice_index = None
        self._not_sorted_children = []

    @property
    def current_children(self):
        return self._current_children

    def get_choice_index(self):
        return self._choice_index

    def _set_child(self, type_, tag, value):
        if value is not None and not isinstance(value, type_):
            value = type_(value)

        current_xml_children = self.current_children
        if value:
            for xml_child in current_xml_children:
                if isinstance(xml_child, type_):
                    self.current_dtd_choice.remove_xml_child(xml_child)

            self.add_xml_child(value)

        name = '_' + replace_dash(tag)

        self.__setattr__(name, value)

    @property
    def current_dtd_choice(self):
        if self._old_choice_index != self._choice_index:
            self._current_choice = self.dtd.get_choices()[self._choice_index].carbon_copy()
            self._old_choice_index = self._choice_index
        return self._current_choice

    def goto_next_dtd_choice(self):
        try:
            old_xml_children = self._not_sorted_children
            self._not_sorted_children = []
            self._choice_index += 1

            for old_xml_child in old_xml_children:
                self.add_xml_child(old_xml_child)
        except IndexError:
            raise StopIteration()

    def check_non_optional(self):
        for leaf in self.current_dtd_choice.traverse_leaves():
            if not leaf.check_min_occurrence():
                raise ChildIsNotOptional(leaf, self)

    def reset_dtd(self):
        self._not_sorted_children = []
        self._current_choice = None
        self._choice_index = 0
        self._old_choice_index = None

    def add_xml_child(self, xml_child):
        choice = self.current_dtd_choice
        selected_leaves = [leaf for leaf in choice.traverse_leaves() if isinstance(xml_child, leaf.type_)]
        # print(selected_leaves)
        if not selected_leaves:
            try:
                self.goto_next_dtd_choice()
                self.add_xml_child(xml_child)
            except Exception:
                raise ChildTypeDTDConflict(xml_child, self)

        else:
            child_added = False
            for selected_leaf in selected_leaves:
                parent = selected_leaf.up
                child_added = selected_leaf.add_xml_child(xml_child)
                if child_added:
                    break

            if not child_added and isinstance(parent, Sequence) and (parent.min_occurrence, parent.max_occurrence) != (
                    1, 1):
                try:
                    parent.pattern
                except AttributeError:
                    parent.pattern = [child.__deepcopy__() for child in parent.get_children()]
                for child in parent.pattern:
                    parent.add_child(child.__deepcopy__())

                child_added = self.add_xml_child(xml_child)

            if not child_added:
                try:
                    self.goto_next_dtd_choice()
                    self.add_xml_child(xml_child)
                except Exception as err:
                    raise ChildOccurrenceDTDConflict(xml_child, self)

            if child_added:
                self.update_current_children()
                self._not_sorted_children.append(xml_child)

            return child_added

    def update_current_children(self):
        self._current_children = self.current_dtd_choice.get_xml_children()

    def add_child(self, child):
        if not self.dtd:
            raise DTDError('_DTD is None. No Child can be added. ')
        self.add_xml_child(child)
        child._up = self
        return child

    def remove_child(self, child):

        current_xml_children = self.current_children
        if child:
            current_xml_children.remove(child)

        self.reset_dtd()

        for xml_child in current_xml_children:
            self.add_xml_child(xml_child)

    def close_dtd(self):
        if self.dtd:
            try:
                self.check_non_optional()
            except ChildIsNotOptional as e:
                try:
                    self.goto_next_dtd_choice()
                    self.close_dtd()
                except (DTDError, StopIteration):
                    raise e
        for child in self.get_children():
            child.close_dtd()

    def get_children(self):
        return self.current_children

    def get_children_by_type(self, type_):
        return [child for child in self.current_children if isinstance(child, type_)]


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
                    raise TypeError('child {} must be of type XMLElement'.format(child))

        set_children()
        if self.text is not None:
            xml.text = str(self.text)
        set_attributes()
        return xml

    def to_string(self):
        self.close_dtd()
        xml = self._to_xml()
        return et.tounicode(xml, pretty_print=True)
